import discord
from discord.ext import commands
from NHentai import NHentai
import xlrd
import xlwt 
from xlwt import Workbook 
import random
import os.path
import string 

# a implementar: 
# .tag => atribui ao user uma tag a um user ao fim de 3x seguidas a sair essa tag tem direito a role.
# .moc => man of culture 
# .hentaime => replaces your pfp on an uglybastard | easteregg de em vez de ugly bastard sair uma cute anime girl

class Profile(commands.Cog):

    def __init__(self,client):
        self.client = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile online\n")

    @commands.command(aliases = ['role'])
    async def tag(self,ctx):

        user_id = ctx.message.author.id
        author = ctx.message.author

        with open('tags.txt', 'r') as f:
            roles = [line.strip() for line in f]

        role = (random.choice(roles)).title()

        if os.path.isfile("cogs/tags.xlsx"):
            print("encontrado")
            
            read_wb = xlrd.open_workbook("cogs/tags.xlsx")
            sheet = read_wb.sheet_by_index(0)

            for i in range(sheet.nrows):
                if sheet.cell_value(0, i) == user_id:
                    print("id encontrado")

                    if (role == sheet.cell_value(1, i)) and ((sheet.cell_value(2, i)) == "2"):
                        print("winner")

                        sheet.write(1,i,role)
                        sheet.write(2,i,"0")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"Congratulations {author}, you just got three roles in a row !!!\n You can now claim your role by asking a mod / admin and providing this message id !")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)

                    elif (role == sheet.cell_value(1,i)):
                        print("same role")

                        sheet.write(1,i,str(int(sheet.cell_value(2, i)) + 1))
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"Two in a row {author}, one more and you win a role !!\nYou dirty {role} lover..")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)

                    else: 
                        print("role updated, user existente")
                        sheet.write(1,i,role)
                        sheet.write(2,i,"0")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"{author}...\nYou filthy {role} lover..")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)

                else: 
                    print("novo user 1")
                    r = (int(sheet.nrows) + 1)

                    sheet.write(0,r,user_id)
                    sheet.write(1,r,role)
                    sheet.write(2,r,"0")
                    
                    embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"**{author}** was just added to our database!\nYou dirty {role} lover...")
                    embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                    await ctx.send(embed=embed)
 
        else:
            print("não encontrado\nficheiro criado\n")
            # caso o ficheiro nao exista cria um novo
            wb = Workbook()
            tagged_list = wb.add_sheet('list of tagged people')
            x,y = 0,0

            tagged_list.write(x,y,user_id)
            tagged_list.write(x,y+1,role)
            tagged_list.write(x,y+2,"1")

            x += 1 
            wb.save("cogs/tags.xlsx")

            embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"**{author}** was just added to our database!\nYou dirty {role} lover...")
            embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Profile(client))

