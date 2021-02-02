import os.path
import random
import string

import discord
import xlrd
import xlwt
from discord.ext import commands
from NHentai import NHentai
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Workbook

# a implementar: 
# .moc => man of culture 
# .hentaime => replaces your pfp on an uglybastard | easteregg de em vez de ugly bastard sair uma cute anime girl

# Checks if the log file (.xlsx) already exists.
def file_exists(p): 
    if os.path.isfile(p): # p is where the file is.
        return True
    else: 
        return False

# Compiles every user id of a sheet into a list.
def get_id(path):
    wb = open_workbook(path,formatting_info=True)
    sheet = wb.sheet_by_index(0)

    id_list = [sheet.cell_value(i,0) for i in range(sheet.nrows)]
    #print(id_list)
    return id_list

# This is where the cog starts.
class Profile(commands.Cog):

    def __init__(self,client):
        self.client = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile online\n")
    
    @commands.command()
    async def role(self, ctx):

        user_id = ctx.message.author.id # Id of the user who called the command.
        author = ctx.message.author # Name of the user who called the command.

        # Opens tags.txt and converts every word into a list.
        with open('cogs/tags.txt', 'r') as f:
            roles = [line.strip() for line in f]

        role = random.choice(roles).title # Random role from the roles list.

        # Checks if the log file already exists, if it does then writes onto it otherwise creates a new one.
        if (file_exists("cogs/lp.xlsx")):

            rb = open_workbook("cogs/lp.xlsx",formatting_info=True) # Opens the log file for read only.
            r_sheet = rb.sheet_by_index(0) # Reads the sheet whoose index is 0. 
        
            wb = copy(rb) # Creates a writable version of rb (I can't read values out of this, only write to it).
            w_sheet = wb.get_sheet(0) # The sheet to write to within the writable copy.
        
            id_list = get_id("cogs/lp.xlsx") # Gets a list of all already existing id's.
            
            # Iterates through every possible row.
            for y in range(r_sheet.nrows):
            
                # Compares user_id with the cell value (ID's : col 0 | Roles : col 1 | Times : col 2)
                if (user_id == r_sheet.cell_value(y,0)):
                    print(f"user já existente {user_id}") # debug

                    # Checks if the times values is equal to three, if so the user wins a role.
                    if (role == r_sheet.cell_value (y,1)) and (int(r_sheet.cell_value(y,2)) == 2):
                        print("winner") # debug
                        
                        # Update the sheet and post the embed on discord.
                        w_sheet.write(y,2,"0")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"Looks like we have a winner!\nCongratulations **{author}** you can now claim your role!")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                    
                    # Checks if the role is same and updates the times value.
                    elif (role == r_sheet.cell_value (y,1)): 
                        print("2 in a row")

                        w_sheet.write(y,2,str(int(r_sheet.cell_value(y,2)) + 1))
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"Two in a row **{author}** !!\nYou dirty {role} lover...")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                    
                    # Updates the new role on the user.
                    else: 
                        print("nova role, adicionar")

                        w_sheet.write(y,1,role)
                        w_sheet.write(y,2,"1")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"You dirty {role} lover...")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break

                # If the user doesn't exist within the log file it adds him to it (and his role, id and times).                
                else: 
                    if (not (user_id in id_list)): # Checks if the user_id is within all the already existing id's.
                        print("user nao existe")
                        r = int(r_sheet.nrows)

                        # Adds the new user.
                        w_sheet.write(r,0,user_id)
                        w_sheet.write(r,1,role)
                        w_sheet.write(r,2,"1")
                        embed = discord.Embed(title=role, colour=discord.Colour.gold(), description=f"**{author}** was just added to our database!\nYou dirty {role} lover...")
                        embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                        await ctx.send(embed=embed)
                        break
                    else: 
                        # Nothing happens until the loop has ended to prevent from multiple entries.
                        pass
            
            # Saves the file, overlapping it.
            wb.save("cogs/lp.xlsx")
        
        # If the file doesn't exist then it creates a new one, already writing the user, role and times.
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

# Loads the cog to the client.
def setup(client):
    client.add_cog(Profile(client))



