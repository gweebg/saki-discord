import discord
from discord.ext import commands
from NHentai import NHentai
import string
import datetime

nhentai = NHentai()
formated_tags = ""

def format_tags(tags):
    global formated_tags
    for elem in tags:
        formated_tags += '['+elem+'] '

def checkRange(l,h,num):
   if l <= num <= h:
       return True
   else:
       return False

def verify_date(data): 
    date = list(data) # 13/07/02 -> ["1","3","/","0","7","/","0","2"]
    date = list(filter(lambda a: a.isdigit() ,date)) # ["1","3","/","0","7","/","0","2"] -> ["1","3","0","7","0","2"]

    if len(date) != 6: 
        print('data com formato inválido') # debug
        raise Exception('Invalid Format')
    else: 
        pass

    day = int(date[0] + date[1])
    month = int(date[2] + date[3])
    year = int(date[4] + date[5]) 

    date = [day,month,year] # debug
    # print(date) # debug 
    
    high = [1,3,5,7,8,10,12] # months with 31 days

    if month in high: 
        
        if checkRange(1,31,day) : 
            if checkRange(1,12,month):
                if checkRange(0,99,year):
                    print("data válida")
                    return True
                else: 
                    print('ano fora dos limites | 31 ano') # debug
                    raise Exception('Invalid Format')
            else:
                print('mes fora dos limites | 31 mes ') # debug
                raise Exception('Invalid Format')
        else:
            print('dia fora dos limites | 31 dia') # debug
            raise Exception('Invalid Format')

    elif (month == 2): 

        if checkRange(1,29,day): 
            if checkRange(1,12,month):
                if checkRange(0,99,year):
                    print("data válida")
                    return True
                else: 
                    print('dia fora dos limites | 31') # debug
                    raise Exception('Invalid Format')
            else:
                print('dia fora dos limites | fev') # debug
                raise Exception('Invalid Format')
        else:
            print('dia fora dos limites | fev') # debug
            raise Exception('Invalid Format')
    
    else: 

        if checkRange(1,30,day): 
            if checkRange(1,12,month):
                if checkRange(0,99,year):
                    print("data válida")
                    return True
                else: 
                    print('dia fora dos limites | 31') # debug
                    raise Exception('Invalid Format')
            else:
                print('dia fora dos limites | fev') # debug
                raise Exception('Invalid Format')
        else:
            print('dia fora dos limites | fev') # debug
            raise Exception('Invalid Format')

    print(date) # debug 
        
class Main(commands.Cog):

    def __init__(self,client):
        self.client = client
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Yoshida-san is ready to be used!")

    @commands.has_role("NSFW")

    @commands.command(aliases = ['r'])
    async def random(self, ctx):
        random_doujin: dict = nhentai.get_random()

        title = random_doujin.get('title')
        tags = random_doujin.get('tags')
        image = random_doujin.get('images')[0]
        id_ = random_doujin.get("id")

        try:
            author = random_doujin.get('artists')[0]

        except IndexError: 
            author = "Unknown"
            
        format_tags(tags)

        embed = discord.Embed(title = title, colour = discord.Colour.gold(), description = "Made by " + author.title(), timestamp = datetime.datetime.now())
        embed.set_image(url = image)
        embed.set_author(name = "Saki Yoshida\n", url = "https://github.com/gweebg/saki-bot", icon_url = "https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")
        embed.set_footer(text = "All information retrieved from nhentai.to")

        embed.add_field(name = "Tags:", value = formated_tags.title(), inline = False)
        embed.add_field(name = "Link:", value = f"[Click me! [NSFW]](https://nhentai.to/g/{id_}/)",inline = False)
        embed.add_field(name = "ID:", value = id_, inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases = ['h'])
    async def hentai(self, ctx, arg):
        global formated_tags

        try:
            verify_date(arg) 

            # formatar o arg (dd/mm/yy)
            special_number = (''.join(list(filter(lambda a: a.isdigit() ,arg)))) # "ddmmyy" 

            if special_number[0] == '0': 
                special_number = int(special_number[1:]) # 01/02/13 -> 10213
            else: 
                special_number = int(special_number) # 11/02/13 -> 110213

            try:
                doujin : dict = nhentai._get_doujin(id = special_number)

                tags = doujin.get("tags")
                format_tags(tags)
                title = doujin.get("title")

                try:
                    artist = doujin.get("artists")[0]

                except IndexError:
                    artist = "Unknown"

                image_main = doujin.get("images")[0]
                embed = discord.Embed(title = title, colour = discord.Colour.gold(), description = "Made by " + artist.title(), timestamp = datetime.datetime.now())

                embed.set_image(url = image_main)
                embed.set_author(name = "Saki Yoshida Bot\n", url = "https://github.com/gweebg/saki-bot", icon_url = "https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")
                embed.set_footer(text = "All information retrieved from nhentai.to")

                embed.add_field(name = "Tags:", value = formated_tags.title(), inline = False)
                embed.add_field(name = "Link:", value = f"[Click me! [NSFW]](https://nhentai.to/g/{special_number}/)",inline = False)
                embed.add_field(name = "ID:", value = special_number, inline = False)

                await ctx.send(embed = embed)


            except AttributeError: 

                if special_number.isdigit() == True:

                    print(f">> {special_number} is not a valid date.")

                    embed = discord.Embed(title="Doujin not found! ", colour=discord.Colour.red(), description="Unfortunately (or not), the date that you submited hasn't still got a doujin number! Try again in a few years?")
                    embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                    await ctx.send(embed=embed)
            

                else: 

                    print(f">> {special_number} is not a date.")
                    
                    embed = discord.Embed(title="Date format unvalid! ", colour=discord.Colour.red(), description="The date format you submited is not valid. Check .help for more information!")
                    embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                    await ctx.send(embed=embed)

        except: 
            embed = discord.Embed(title="Date format unvalid! ", colour=discord.Colour.red(), description="The date format you submited is not valid. Check .help for more information!")
            embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

            await ctx.send(embed=embed)
            
    @commands.command(aliases = ['s'])
    async def search(self, ctx, id):
        try:
            search_obj: dict = nhentai.search(query = id, sort='popular', page=1)
            
            title = search_obj.get("title")
            tags = search_obj.get("tags")
            image = search_obj.get("images")[0]

            format_tags(tags)

            try: 
                artist = search_obj.get("artists")[0]
            
            except IndexError: 
                artist = "Unknown"
            
            embed = discord.Embed(title = title, colour = discord.Colour.gold(), description = "Made by " + artist.title(), timestamp = datetime.datetime.now())

            embed.set_image(url = image)
            embed.set_author(name = "Saki Yoshida Bot\n", url = "https://github.com/gweebg/saki-bot", icon_url = "https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")
            embed.set_footer(text = "All information retrieved from nhentai.to")

            embed.add_field(name = "Tags:", value = formated_tags.title(), inline = False)
            embed.add_field(name = "Link:", value = f"[Click me! [NSFW]](https://nhentai.to/g/{id}/)",inline = False)
            embed.add_field(name = "ID:", value = id, inline = False)

            await ctx.send(embed = embed)

        except: 
            try:
                id = int(id)
                embed = discord.Embed(title="Not a doujin!", colour=discord.Colour.red(), description="The number that was provided has not 'received' a doujin yet.\n Try another one!")
                embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                await ctx.send(embed=embed)
            except: 
                embed = discord.Embed(title="Not a number! ", colour=discord.Colour.red(), description="To use the search command you need to provide a number (bellow 6 digits)!")
                embed.set_author(name="Saki Yoshida", url="https://github.com/gweebg/saki-bot", icon_url="https://pbs.twimg.com/profile_images/1040256267007090688/ZrXrHE33_400x400.jpg")

                await ctx.send(embed=embed)
            
def setup(client):
    client.add_cog(Main(client))

    