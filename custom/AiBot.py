from ananas import PineappleBot, ConfigurationError, hourly
import archiveis
import logging
from bs4 import BeautifulSoup, SoupStrainer
from dd_client import DD

class AiBot(PineappleBot):
    def start(self):
        print("start")
        if "account" not in self.config: raise ConfigurationError("Bot requires an 'account'")
        accounts = self.mastodon.account_search(
            q = self.config.account,
            limit = 1
        )
        self.bot = accounts[0]
        self.dd = DD(self.config.dd_host, int(self.config.dd_port), 0, path = self.config.dd_path)
        self.dd.set_return_format(0)

    def get_followers(self, account):
        return self.mastodon.account_followers(account.id)

    def get_follower_statuses(self, follower):
        return self.mastodon.account_statuses(follower.id)

    def get_status_replies(self, status):
        return self.mastodon.status_context(status.id).descendants

    def reply_to_status(self, status, message):
        self.mastodon.status_post(message, in_reply_to_id = status)

    def predict(self, serviceName, status):

        message = BeautifulSoup(status.content, features="lxml")
        data = [message.get_text(separator=' ').replace("http://", "").replace("https://", "")]

        parameters_input = {"confidence_threshold":0.3}
        parameters_mllib = {}
        parameters_output = {}

        return self.dd.post_predict(
            serviceName,
            data,
            parameters_input,
            parameters_mllib,
            parameters_output
        )

    def actionOnStatus(self, status):

        predict = self.predict(self.config.dd_service_name, status)

        classInfo = predict['body']['predictions'][0]['classes'][0]

        outputMessage = "sent_en - {1} - {2:3.2f}".format(self.config.dd_service_name, classInfo['cat'], classInfo['prob'])

        print(outputMessage)

        try:
            self.reply_to_status(status, outputMessage)
        except Exception:
            logger.exception("Error when posting a reply")

    @hourly(minute=51)
    def hourlyActionOnFollowersToots(self):
        print("hourly")

        for follower in self.get_followers(self.bot):

            for status in self.get_follower_statuses(follower):

                replies = self.get_status_replies(status)
                replies_accounts = [r.account.acct for r in replies]

                if status["replies_count"] == 0 or self.config.account not in replies_accounts:

                    self.actionOnStatus(status)
