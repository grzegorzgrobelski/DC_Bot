import discord
from discord.ext import commands
import re
import json


token= '' 
command_prefix_global = '--- '


intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True 
bot = commands.Bot(command_prefix = command_prefix_global,intents=intents)


thread_lifetime = 60 #Czas po którym thread znika bez aktywnosci
# Mozliwe wartosci do wyboru: (W innych przypadkach bot nie zadziala)
# 60 dla 1 godziny
# 1440 dla 24 godzin
# 4320 dla 3 dni
# 10080 dla 7 dni

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

    if existing_thread :
        await existing_thread.add_user(ctx.author)
        return

    description = description_template.format(
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
    )

    initial_message = await ctx.channel.send(description or "No description provided.")
    thread = await initial_message.create_thread(name=thread_name, auto_archive_duration=thread_lifetime) 
    #thread = await ctx.create_thread(name=thread_name, auto_archive_duration=thread_lifetime) 
    # description_message = await thread.send(
    #     description_template.format(
    #         first_row='',
    #         second_row='',
    #         third_row='',
    #         fourth_row='',
    #         fifth_row='',
    #         sixth_row='',
    #         seventh_row='',
    #         eighth_row='',
    #         ninth_row='',
    #         tenth_row=''
    #     ))
    # await description_message.pin()
    await thread.add_user(ctx.author)


async def change_thread_description(ctx, new_comment: str):
    if isinstance(ctx.channel, discord.Thread) and check_pattern(new_comment):
        parent_channel = ctx.channel.parent
        parent_message_id = ctx.channel.id  # This ID is the same as the thread ID
        parent_message = await parent_channel.fetch_message(parent_message_id)

        if parent_message:
            desc = modify_description(parent_message.content,new_comment,ctx.author.display_name)
            await parent_message.edit(content=desc)


# async def change_thread_description(ctx, new_comment: str):
#     if isinstance(ctx.channel, discord.Thread) and check_pattern(new_comment):
#         messages = ctx.channel.history(oldest_first = True, limit= 2)
#         #print(new_comment)
#         async for message in messages:
#             if message.type == discord.MessageType.default:
#                 if message.author == bot.user:
#                     test = modify_description(message.content,new_comment,ctx.author.display_name)
#                     await message.edit(content = test) 
#                     return

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




# def modify_description(description,given_comment = '+1.1', given_nick = 'Test'):
#     rows = [[None], [None], [None], [None], [None], [None], [None], [None], [None], [None]]
#     if description[-1] == ':': description = description+ ' ' #To jeszcze do sprawdzenia
#     description_rows = description.split("\n") 
#     for i in range(10):
#         extracted_nicks = description_rows[i].split(": ")[1].split(",")
#         if len(extracted_nicks) > 0:
#             for j, nick in enumerate(extracted_nicks):
#                 if len(rows[i]) > j:
#                     rows[i][j] = nick
#                 else:
#                      rows[i].append(nick)
                
#     rows = row_modyfication(rows,given_comment,given_nick)


#     return description_template.format(
#         first_row= ','.join(rows[0]) if rows[0][0] != '' and rows[0][0] != None else '',
#         second_row= ','.join(rows[1]) if rows[1][0] != '' and rows[1][0] != None else '',
#         third_row= ','.join(rows[2]) if rows[2][0] != '' and rows[2][0] != None else '',
#         fourth_row=','.join(rows[3]) if rows[3][0] != '' and rows[3][0] != None else '',
#         fifth_row=','.join(rows[4]) if rows[4][0] != '' and rows[4][0] != None else '',
#         sixth_row=','.join(rows[5]) if rows[5][0] != '' and rows[5][0] != None else '',
#         seventh_row=','.join(rows[6]) if rows[6][0] != '' and rows[6][0] != None else '',
#         eighth_row=','.join(rows[7]) if rows[7][0] != '' and rows[7][0] != None else '',
#         ninth_row=','.join(rows[8]) if rows[8][0] !='' and rows[8][0] != None else '',
#         tenth_row=','.join(rows[9]) if rows[9][0] != '' and rows[9][0] != None else '',
#     )



def row_modyfication(table,comment,nick):
    action_type = comment[0]
    affected_row = int(comment[1:].split('.')[0]) -1  
    affected_positiom = int(comment[1:].split('.')[1]) -1
    
    if action_type == '+':
        if table[affected_row] == ['']:
            table[affected_row][0] = nick 
        else:
            if nick not in table[affected_row]:
                if affected_positiom < len(table[affected_row]):
                    table[affected_row].insert(affected_positiom,nick)
                else:
                    table[affected_row].append(nick)
            else:
                table[affected_row].remove(nick)
                table[affected_row].insert(affected_positiom,nick)
        return table
    
    elif action_type == '-':
        table_affected_row_len = len(table[affected_row])
        if table[affected_row] != [''] and table_affected_row_len != 1 and table_affected_row_len > affected_positiom :
            table[affected_row].pop(affected_positiom) 
        elif table_affected_row_len == 1 and affected_positiom == 0: 
            table[affected_row][0] =''

    return table
def check_pattern(s):
    if s and s[0] in ['+', '-']:
        pattern = r'^[+-]?\d+\.\d+$'
        match = re.match(pattern, s)
        return match is not None
    else:
        return False
def get_token():
    if token != '':
        return str(token)
    else:
        with open('config.json') as config_file:
            config = json.load(config_file)
            return str(config['token'])




bot.run(get_token())