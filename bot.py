import discord
from discord.ext import commands
from discord.ui import Button, View
import aiohttp
import asyncio

# 機器人的令牌
TOKEN = 'Your-Token'
# 後端 API URL
BACKEND_URL = 'http://localhost:3000/register'

# 創建 intents 以指定你想要接收的事件
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # 確保這個意圖被啟用以接收消息內容

# 創建機器人實例並傳遞 intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

class RoleAssignmentView(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="教職員", style=discord.ButtonStyle.primary)
    async def school_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        guild = interaction.guild       
        # 獲取「教職員」身分組
        role_name = "教職員"
        role = discord.utils.get(guild.roles, name=role_name)

        await member.add_roles(role)
        await interaction.response.send_message("你已加入教職員組！", ephemeral=True)
        # 刪除原始訊息
        await interaction.message.delete()
    
    
    @discord.ui.button(label="學生", style=discord.ButtonStyle.primary)
    async def student_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        guild = interaction.guild       
        # 獲取「教職員」身分組
        role_name = "學生"
        role = discord.utils.get(guild.roles, name=role_name)

        await member.add_roles(role)
        await interaction.response.send_message("你已加入學生組！", ephemeral=True)
        # 刪除原始訊息
        await interaction.message.delete()


@bot.command()

async def register(ctx):
    await ctx.send("請輸入編號:",ephemeral=True)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        student_id_msg = await bot.wait_for('message', check=check, timeout=60)
        student_id = student_id_msg.content

        await ctx.send("請輸入姓名:",ephemeral=True)
        name_msg = await bot.wait_for('message', check=check, timeout=60)
        name = name_msg.content

        # 發送數據到後端
        async with aiohttp.ClientSession() as session:
            async with session.post(BACKEND_URL, json={"student_id": student_id, "name": name}) as resp:
                if resp.status == 200:
                    await ctx.send(f"歡迎，{name}！")

                    # 發送帶有按鈕的消息
                    view = RoleAssignmentView()
                    await ctx.send("你是學生還是教職員呢", view=view,ephemeral=True)
                else:
                    await ctx.send("註冊失敗，請稍後再試。")

    except asyncio.TimeoutError:
        await ctx.send("超時未回應，請重新輸入 !register 指令開始註冊。")


# 運行機器人
bot.run(TOKEN)
