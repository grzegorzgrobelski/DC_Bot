import discord
from discord.ext import commands
import asyncio
import re

#Nie zapomniec:
# Wywala sie na ostatnim elemencie bo brakuje mu tam ": " a jest ":"


command_prefix_global = '--- '


# Konfiguracja bota
intents = discord.Intents.default()
intents.messages = True  # to trzeba sprawdzic ocb
intents.message_content = True  # Potrzebne do nasłuchiwania wiadomości
bot = commands.Bot(command_prefix = command_prefix_global,intents=intents)


description_template = """
1. HoJ: {first_row}
2. Def Tank: {second_row}
3. Holy/Nature: {third_row}
4. Hallow: {fourth_row}
5. Astral Staff/GA: {fifth_row}
6. Spirithunter/Carving: {sixth_row}
7. Perma: {seventh_row}
8. Spiked/Riftclave: {eighth_row}
9. Hellfire/Heron: {ninth_row}
10. Carrioncaller/helbeard/scythe/Primal: {tenth_row}
"""






#Chyba ten co tworzy powinien byc dodawany od kopa yoo? []
## dodac zeby nie tworzyc kolejnych watkow jak juz sie jest w watku[]
## Dodac przypianie do pierwszej wiadomosci jako watku []
## Posprawdzac te ctx 





@bot.event
async def on_message(message):
    if message.author == bot.user:  
        return
    
    if isinstance(message.channel, discord.TextChannel) and message.content.startswith(command_prefix_global):
        await create_thread(message, message.content.split(' ')[1])
        return
    elif isinstance(message.channel, discord.Thread) and (message.content.startswith('+') or message.content.startswith('-')):
        await change_thread_description(message, message.content)
        return
    return 

async def create_thread(ctx, thread_name: str):
    existing_thread = discord.utils.find(lambda t: t.name == thread_name, ctx.channel.threads)
    #print(existing_thread.parent)
    #and existing_thread.parent == ctx.channel.name
    if existing_thread :
        await existing_thread.add_user(ctx.author)
        return

    thread = await ctx.create_thread(name=thread_name, auto_archive_duration=1440)  # auto_archive_duration is in minutes (1440 = 24 hours)

    #thread = await ctx.create_thread(name=thread_name, type=discord.ChannelType.public_thread) ## Test purp
    
    #thread = await ctx.channel.create_thread(name=thread_name, type=discord.ChannelType.public_thread) ## Test purp
    #thread = await ctx.channel.create_thread(name=thread_name, type=discord.ChannelType.private_thread)  
   

        #
        #thread = await message.create_thread(name=thread_name, auto_archive_duration=1440)  # auto_archive_duration is in minutes (1440 = 24 hours)

    #messages = thread.history(oldest_first = True, limit= 2)

    # async for message in messages:
    #     message.delete()
    #     if message.type == discord.MessageType.default:
    #         if message.author == bot.user:
    #             print('mleko')
    #             #Switch na te +1.1 -1.2 itd + weryfikacja
    #             #test = modify_description(message.content,new_comment,ctx.author.display_name)
    #             #await message.edit(content = test)  # Edytowanie wiadomości
    #             #await ctx.send("Opis wątku został zmieniony.")
    #           return

    description_message = await thread.send(
        description_template.format(
            first_row='',
            second_row='',
            third_row='',
            fourth_row='',
            fifth_row='',
            sixth_row='',
            seventh_row='',
            eighth_row='',
            ninth_row='',
            tenth_row=''
        ))
    # await description_message.pin()
    # await asyncio.gather(
    #     description_message.pin()
    # )
    await description_message.pin()
    await thread.add_user(ctx.author)


async def change_thread_description(ctx, new_comment: str):
    if isinstance(ctx.channel, discord.Thread) and check_pattern(new_comment):
        messages = ctx.channel.history(oldest_first = True, limit= 2)
        print(new_comment)
        async for message in messages:
            if message.type == discord.MessageType.default:
                if message.author == bot.user:
                    #Switch na te +1.1 -1.2 itd + weryfikacja
                    test = modify_description(message.content,new_comment,ctx.author.display_name)
                    await message.edit(content = test)  # Edytowanie wiadomości
                    #await ctx.send("Opis wątku został zmieniony.")
                    return
        
        # await ctx.send("Nie znaleziono wiadomości w wątku.")
    # else:
    #     await ctx.send("Ta komenda działa tylko w wątkach.")

def modify_description(description,given_comment = '+1.1', given_nick = 'Test'):
    rows = [[None], [None], [None], [None], [None], [None], [None], [None], [None], [None]]
    if description[-1] == ':': description = description+ ' ' #To jeszcze do sprawdzenia
    description_rows = description.split("\n") 
    for i in range(10):
        extracted_nicks = description_rows[i].split(": ")[1].split(",")
        if len(extracted_nicks) > 0:
            for j, nick in enumerate(extracted_nicks):
                if len(rows[i]) > j:
                    rows[i][j] = nick
                else:
                     rows[i].append(nick)
                
    rows = row_modyfication(rows,given_comment,given_nick)


    return description_template.format(
        first_row= ','.join(rows[0]) if rows[0][0] != '' and rows[0][0] != None else '',
        second_row= ','.join(rows[1]) if rows[1][0] != '' and rows[1][0] != None else '',
        third_row= ','.join(rows[2]) if rows[2][0] != '' and rows[2][0] != None else '',
        fourth_row=','.join(rows[3]) if rows[3][0] != '' and rows[3][0] != None else '',
        fifth_row=','.join(rows[4]) if rows[4][0] != '' and rows[4][0] != None else '',
        sixth_row=','.join(rows[5]) if rows[5][0] != '' and rows[5][0] != None else '',
        seventh_row=','.join(rows[6]) if rows[6][0] != '' and rows[6][0] != None else '',
        eighth_row=','.join(rows[7]) if rows[7][0] != '' and rows[7][0] != None else '',
        ninth_row=','.join(rows[8]) if rows[8][0] !='' and rows[8][0] != None else '',
        tenth_row=','.join(rows[9]) if rows[9][0] != '' and rows[9][0] != None else '',
    )

def row_modyfication(table,comment,nick):
    action_type = comment[0]
    affected_row = int(comment[1]) -1   #Dodac Handlowanie do obu /Tak zeby wylapac jakby jakies  cos innego niz numer byl ale tez jezlei < 0 jest
    affected_positiom = int(comment[3:-1])-1 if len(comment) > 4 else int(comment[-1])-1
    
    if action_type == '+':
        if table[affected_row] == ['']:
            table[affected_row][0] = nick  # Jeśli lista jest pusta, przypisz nick do pierwszego elementu
        else:
            if nick not in table[affected_row]: ## Unikamy duplikatow
                if affected_positiom < len(table[affected_row]):
                    table[affected_row].insert(affected_positiom,nick)
                else:
                    table[affected_row].append(nick)  # Jeśli lista nie jest pusta, dodaj nick na koniec listy 
            else: #Jest juz w tej liscie ale jest dalej niz zerowy element
                table[affected_row].remove(nick)
                table[affected_row].insert(affected_positiom,nick)
                print('trzeba go przeniesc')

            #Tutaj trzeba będzie dopisac kod ktory przeniesie usera na koneic np listy 
        return table
    
    elif action_type == '-':
        table_affected_row_len = len(table[affected_row])
        if table[affected_row] != [''] and table_affected_row_len != 1 and table_affected_row_len > affected_positiom : #Trzeba sprawdzic czy nie usuwamy kogos z poza listy
            #table[affected_row].remove(nick) ## Trzeba zobaczyc co sie stanie jak w srodku wytniesz
            table[affected_row].pop(affected_positiom) ## Trzeba zobaczyc co sie stanie jak w srodku wytniesz
        elif table_affected_row_len == 1 and affected_positiom == 0:  #table[affected_row] == [''] and 
            table[affected_row][0] =''

    return table

def check_pattern(s):
    if s and s[0] in ['+', '-']:
        pattern = r'^[+-]?\d+\.\d+$'
        match = re.match(pattern, s)
        return match is not None
    else:
        return False
    
   

bot.run('')