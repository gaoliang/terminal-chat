import os
import datetime
import redis
import json


class Chat:
    def __init__(self, name, chanel):
        self.name = name
        self.r = redis.StrictRedis()
        self.ps = self.r.pubsub()
        self.chanel = chanel
        self.start()

    def message_handle(self, message):
        message = json.loads(message['data'])
        output = '[{} {}]: {}'.format(
            message['user'], message['time'], message['content']
        )
        if message['user'] == self.name:
            output = output.rjust(os.get_terminal_size().columns)
        print(output)

    def send_message(self, content):
        message = {
            'content': content,
            'user': self.name,
            'time': datetime.datetime.now().strftime('%H:%M:%S')
        }
        self.r.publish(self.chanel, json.dumps(message))

    def start(self):
        self.ps.subscribe(**{chanel: self.message_handle})
        subscriber_count = self.r.execute_command('PUBSUB', 'NUMSUB', chanel)[1]
        print('Welcome! Now {} pepole on the channel.'.format(subscriber_count))
        thread = self.ps.run_in_thread(sleep_time=0.001)
        try:
            while True:
                content = input()
                print("\033[A                             \033[A")  # 删除刚刚的输入行
                self.send_message(content)
                # 这行代码用来推送mac的系统通知消息
                # os.system(f"""osascript -e 'display notification "{raw_message}" with title "{user}"'""")
        except KeyboardInterrupt:  # 退出
            print("exit!")
        finally:
            thread.stop()


if __name__ == "__main__":
    username = input('Enter your name:\n')
    chanel = input('Enter chanel:\n')
    Chat(username, chanel)
