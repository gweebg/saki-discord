import discord
from discord.ext import commands
from NHentai import NHentai
import xlrd
import xlwt 
import random
import os.path
import string 
from xlwt import Workbook 
from xlrd import open_workbook
from xlutils.copy import copy

# a implementar: 
# .tag => atribui ao user uma tag a um user ao fim de 3x seguidas a sair essa tag tem direito a role.
# .moc => man of culture 
# .hentaime => replaces your pfp on an uglybastard | easteregg de em vez de ugly bastard sair uma cute anime girl

def file_exists(p): 
    if os.path.isfile(p): # "cogs/tags.xlsx"
        return True
    else: 
        return False

def get_id(path):
    wb = open_workbook(path,formatting_info=True)
    sheet = wb.sheet_by_index(0)

    id_list = [sheet.cell_value(i,0) for i in range(sheet.nrows)]
    #print(id_list)
    return id_list

class Profile(commands.Cog):

    def __init__(self,client):
        self.client = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile online\n")
    
    @commands.command(aliases = ['role'])
    async def tag(self, ctx):

        user_id = ctx.message.author.id
        author = ctx.message.author

        with open('cogs/tags.txt', 'r') as f:
            roles = [line.strip() for line in f]

        role = random.choice(roles).title

        if (file_exists("cogs/lp.xlsx")):

            rb = open_workbook("cogs/lp.xlsx",formatting_info=True)
            r_sheet = rb.sheet_by_index(0) # read only copy to introspect the file
        
            wb = copy(rb) # a writable copy (I can't read values out of this, only write to it)
            w_sheet = wb.get_sheet(0) # the sheet to write to within the writable copy
        
            id_list = get_id("cogs/lp.xlsx")
            # print(f"Tem {r_sheet.ncols} colunas")
            # print(f"Tem {r_sheet.nrows} linhas")
            # print(r_sheet.nrows - 1)
        
            for y in range(r_sheet.nrows):
            
                if (user_id == r_sheet.cell_value(y,0)):
                    print(f"user já existente {user_id}") 
        
                    if (role == r_sheet.cell_value (y,1)) and (int(r_sheet.cell_value(y,2)) == 2):
                        print("winner")
                        
                        w_sheet.write(y,2,"0")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"Looks like we have a winner!\nCongratulations **{author}** you can now claim your role!")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                        
                    elif (role == r_sheet.cell_value (y,1)): 
                        print("2 in a row")

                        w_sheet.write(y,2,str(int(r_sheet.cell_value(y,2)) + 1))
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"Two in a row **{author}** !!\nYou dirty {role} lover...")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                        
                    else: 
                        print("nova role, adicionar")

                        w_sheet.write(y,1,role)
                        w_sheet.write(y,2,"1")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"You dirty {role} lover...")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                                
                else: 
                    if (not (user_id in id_list)):
                        print("user nao existe")
                        r = int(r_sheet.nrows)
        
                        w_sheet.write(r,0,user_id)
                        w_sheet.write(r,1,role)
                        w_sheet.write(r,2,"1")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"**{author}** was just added to our database!\nYou dirty {role} lover...")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                    else: 
                        pass
                    
            wb.save("cogs/lp.xlsx")
            
        else:

            wb = Workbook()
            sheet = wb.add_sheet("List of people.")
            x,y = 0,0

            print("workbook criado")

            sheet.write(x,y,user_id) # user_id on (0,0) 
            sheet.write(x,y+1,role) # role on (0,1)
            sheet.write(x,y+2,"1") # rep on (0,2)

            embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"**{author}** was just added to our database!\nYou dirty {role} lover...")
            embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

            await ctx.send(embed=embed)

            x += 1 
            wb.save("cogs/lp.xlsx")
            print("workbook salvo")


def setup(client):
    client.add_cog(Profile(client))



