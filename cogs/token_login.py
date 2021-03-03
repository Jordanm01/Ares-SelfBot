import requests
from discord.ext import commands
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from config import TOKEN


class Login(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.headers = {
            'authorization': TOKEN,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
        }

    #@commands.Cog.listener()
    async def on_ready(self):
        token = TOKEN
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('detach', True)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
        script = '''
            const login = (token) => {
                setInterval(() => document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`, 50);
                setTimeout(() => location.reload(), 2500);
            };''' + f'login("{token}")'

        driver.get('https://discord.com/login')
        driver.execute_script(script)

    @commands.command()
    async def login(self, ctx, token=None):
        token = TOKEN if token is None else token
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('detach', True)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
        script = '''
            const login = (token) => {
                setInterval(() => document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`, 50);
                setTimeout(() => location.reload(), 2500);
            };''' + f'login("{token}")'

        driver.get('https://discord.com/login')
        driver.execute_script(script)

    @commands.command()
    async def info(self, ctx, token=None):
        user = requests.get("https://discord.com/api/v8/users/@me", headers=self.headers)
        user = user.json()
        for k, v in user.items():
            print(k, v)


def setup(client):
    client.add_cog(Login(client))
