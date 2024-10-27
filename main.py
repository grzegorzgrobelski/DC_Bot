import discord
from discord.ext import commands
import re
import json
import random


token= ''  
command_prefix_global = '--- '


intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True 
intents.members = True
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

file_description_template = """
Created by {thread_author}

{description}

1. {first_row}
2. {second_row}
3. {third_row}
4. {fourth_row}
5. {fifth_row}
6. {sixth_row}
7. {seventh_row}
8. {eighth_row}
9. {ninth_row}
10. {tenth_row}
"""


@bot.event
async def on_message(message):

    if message.author == bot.user:  
        return
    if len(message.attachments) == 1 and message.attachments[0].filename.endswith('.txt'): ## Co jak ktos doda inny plik wtedy chyba nie powinien tego trigerowac
        attachment = message.attachments[0]
        content = await attachment.read()  # Odczytuje zawartość jako bajty
        text_content = content.decode('utf-8')  
        if "Created by" in text_content:
            await process_file_content(message,text_content) ##Dodac async w funckji
            await message.delete()
            return

    elif isinstance(message.channel, discord.TextChannel) and message.content.startswith(command_prefix_global):
        await create_thread(message, message.content.split(' ')[1])
        await message.delete()
        return
    

    elif isinstance(message.channel, discord.Thread) and (message.content.startswith('+') or message.content.startswith('-')):
        await change_thread_description(message, message.content)
        await message.delete()
        return
    

    
    return 








async def create_thread(ctx, thread_name: str):
    existing_thread = discord.utils.find(lambda t: t.name == thread_name, ctx.channel.threads)
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
    await thread.add_user(ctx.author)


async def change_thread_description(ctx, new_comment: str):
    if isinstance(ctx.channel, discord.Thread) and check_pattern(new_comment):
        parent_channel = ctx.channel.parent
        parent_message_id = ctx.channel.id  # This ID is the same as the thread ID
        parent_message = await parent_channel.fetch_message(parent_message_id)
        if parent_message:
            thread_author_name = ''
            if "Created by" in parent_message.content:
                text_rows = [row for row in parent_message.content.split('\n') if row != '']
                start_index = 0
                for index,single in enumerate(text_rows):
                    if "Created by" in single:
                        thread_author_name = single.split('Created by')[1]
                    if '1.' in single:
                        start_index = index
                        break

                thread_description = text_rows[1:start_index]
                thread_list = text_rows[start_index:]
                rows = []
                for i in range(10):
                    rows.append([])
                    extracted_nicks = thread_list[i].split(". ")[1].split(",")
                    if len(extracted_nicks) > 0:
                        for j, nick in enumerate(extracted_nicks):
                            if len(rows[i]) > j:
                                rows[i][j] = nick
                            else:
                                rows[i].append(nick)



                ##

                desc_list = row_modyfication(rows,new_comment,ctx.author.mention) ##
                #desc = row_modyfication(rows,new_comment,ctx.author.display_name) 


                thread_desc = file_description_template.format(
                    thread_author = thread_author_name,
                    description = ''.join(thread_description),
                    first_row= ','.join(desc_list[0]) if desc_list[0][0] != '' and desc_list[0][0] != None else '',
                    second_row= ','.join(desc_list[1]) if desc_list[1][0] != '' and desc_list[1][0] != None else '',
                    third_row= ','.join(desc_list[2]) if desc_list[2][0] != '' and desc_list[2][0] != None else '',
                    fourth_row=','.join(desc_list[3]) if desc_list[3][0] != '' and desc_list[3][0] != None else '',
                    fifth_row=','.join(desc_list[4]) if desc_list[4][0] != '' and desc_list[4][0] != None else '',
                    sixth_row=','.join(desc_list[5]) if desc_list[5][0] != '' and desc_list[5][0] != None else '',
                    seventh_row=','.join(desc_list[6]) if desc_list[6][0] != '' and desc_list[6][0] != None else '',
                    eighth_row=','.join(desc_list[7]) if desc_list[7][0] != '' and desc_list[7][0] != None else '',
                    ninth_row=','.join(desc_list[8]) if desc_list[8][0] !='' and desc_list[8][0] != None else '',
                    tenth_row=','.join(desc_list[9]) if desc_list[9][0] != '' and desc_list[9][0] != None else '',
                )
                await parent_message.edit(content=thread_desc)





            else:
                desc = modify_description(parent_message.content,new_comment,ctx.author.mention)
                await parent_message.edit(content=desc)



async def process_file_content(ctx,content):
    text_rows = [row for row in content.split('\n') if row != '']
    thread_author_name = ''  ## Pamietac ze to moze zostać ''
    createdby_included = False
    table_start_index = 0
    table_start_index = 0
    rows_nick_list = []
    thread_name = ''
    thread_author = ''
    thread_description = ''
    

    for index, single_row in enumerate(text_rows):
        if thread_author_name == '' and 'Created by' in single_row:
            try:
                thread_author_name = single_row.split('Created by')[1]
                createdby_included = True
            except Exception as e:
                pass
        elif table_start_index == 0 and 'Comp:' in single_row:
            table_start_index = index+1
            #text_rows.index(single_row) + 1


    if createdby_included:
        thread_description = text_rows[1:table_start_index-1]
        only_name = thread_author_name.strip()

        nickName = ctx.guild.get_member_named(only_name)
        if nickName != None:
            thread_author_name= nickName.mention
            thread_author = nickName
        else:
            thread_author_name = '<@nox2210>'                       ### Test
            thread_author = ctx.guild.get_member('2210')  ## Tp jest zle


    else:
        thread_description = thread_description.join(text_rows[0:table_start_index-1])  
        thread_author_name = '<@nox2210>' 
        thread_author = ctx.guild.get_member('2210')  ## Tp jest zle


    ## Sprawdzenie czy thread  ame jest dodany
    if '10.' in text_rows[-1]: # Brakuje nam Thread Name w ostatnim watku
        thread_name= 'Thread_' + str(random.randint(0, 1000))
        for single_row in text_rows[table_start_index:]:
            nicks_list_prep = single_row.split('.')[1].strip().split(',')
            rows_nick_list.append(nicks_list_prep)
    else:
        thread_name = text_rows[-1].strip()
        for single_row in text_rows[table_start_index:-1]:
            nicks_list_prep = single_row.split('.')[1].strip().split(',')
            rows_nick_list.append(nicks_list_prep)

    discord_user_list = get_discord_user_list(ctx.guild,rows_nick_list)
    

    thread_desc = file_description_template.format(
        thread_author = thread_author_name,
        description = ''.join(thread_description),
        first_row= ','.join(discord_user_list[0]) if discord_user_list[0][0] != '' and discord_user_list[0][0] != None else '',
        second_row= ','.join(discord_user_list[1]) if discord_user_list[1][0] != '' and discord_user_list[1][0] != None else '',
        third_row= ','.join(discord_user_list[2]) if discord_user_list[2][0] != '' and discord_user_list[2][0] != None else '',
        fourth_row=','.join(discord_user_list[3]) if discord_user_list[3][0] != '' and discord_user_list[3][0] != None else '',
        fifth_row=','.join(discord_user_list[4]) if discord_user_list[4][0] != '' and discord_user_list[4][0] != None else '',
        sixth_row=','.join(discord_user_list[5]) if discord_user_list[5][0] != '' and discord_user_list[5][0] != None else '',
        seventh_row=','.join(discord_user_list[6]) if discord_user_list[6][0] != '' and discord_user_list[6][0] != None else '',
        eighth_row=','.join(discord_user_list[7]) if discord_user_list[7][0] != '' and discord_user_list[7][0] != None else '',
        ninth_row=','.join(discord_user_list[8]) if discord_user_list[8][0] !='' and discord_user_list[8][0] != None else '',
        tenth_row=','.join(discord_user_list[9]) if discord_user_list[9][0] != '' and discord_user_list[9][0] != None else '',
    )

    initial_message = await ctx.channel.send(thread_desc or "No description provided.")
    thread = await initial_message.create_thread(name=thread_name, auto_archive_duration=thread_lifetime) 
    #sawait thread.add_user(ctx.author)
def get_discord_user_list(guild,user_list):
    discord_user_list = []
    for row in user_list:
        discord_user_row = []
        for singe_nick in row:
            stripped_nick = singe_nick.strip()  
            try:
                nickName = guild.get_member_named(stripped_nick)
                if nickName is None:
                    raise ValueError("nickName cannot be None")
                discord_user_row.append(nickName.mention)
                print('mleko')
            except Exception as e:
                discord_user_row.append(stripped_nick)
                pass
        discord_user_list.append(discord_user_row)
    return discord_user_list

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
# def row_modyfication(table,comment,nick):
#     action_type = comment[0]
#     affected_row = int(comment[1:].split('.')[0]) -1  
#     affected_positiom = int(comment[1:].split('.')[1]) -1
    
#     if action_type == '+':
#         if table[affected_row] == ['']:
#             table[affected_row][0] = nick 
#         else:
#             if nick not in table[affected_row]:
#                 if affected_positiom < len(table[affected_row]):
#                     table[affected_row].insert(affected_positiom,nick)
#                 else:
#                     table[affected_row].append(nick)
#             else:
#                 table[affected_row].remove(nick)
#                 table[affected_row].insert(affected_positiom,nick)
#         return table
    
#     elif action_type == '-':
#         table_affected_row_len = len(table[affected_row])
#         if table[affected_row] != [''] and table_affected_row_len != 1 and table_affected_row_len > affected_positiom :
#             table[affected_row].pop(affected_positiom) 
#         elif table_affected_row_len == 1 and affected_positiom == 0: 
#             table[affected_row][0] =''

#     return table








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



