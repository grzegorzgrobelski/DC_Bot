import re

pattern = re.compile(r"^([1-9][0-9]?)\.")

class FileManager:
    def __init__(self,guild, content):
        self.main_thread_description = ''
        self.file_content = content
        self.thread_author = ''
        self.guild = guild
        self.users_in_description = False
        self.teams = self.process_file_content(self.file_content)
        print('mleczko')
        

# async 
    # def get_discord_user_list(self, row, user_list):
    #     discord_user_list = []
    #     single_user = user_list.split(',')
    #     for index,nick in enumerate(single_user):
    #         stripped_nick = nick.strip() 
    #         try:
    #             nickName = self.guild.get_member_named(stripped_nick)
    #             if nickName is None:
    #                 raise ValueError("nickName cannot be None")
    #             discord_user_list.append((str(row), nickName.mention))
    #             print('mleko')
    #         except Exception as e:
    #             discord_user_list.append((str(row), stripped_nick))
    #     return discord_user_list
    
    def get_discord_user_list(self, row, user_list):
        discord_user_list = []

        single_user = ''
        test_1 = user_list.split('-')
        test_2 = user_list.split(',')
        

        if len(user_list.split('-')) > 1:
            single_user = user_list.split('-')
        else:
            single_user = user_list.split(',')



        how_many_items = len(single_user)
        if how_many_items >= 2:
            try:
                nickName = self.guild.get_member_named(single_user[1].strip())
                if nickName is None:
                    raise ValueError("nickName cannot be None")
                discord_user_list.append((str(row), str(single_user[0]).strip(), nickName.mention.strip()))
            except Exception as e:
                discord_user_list.append((str(row), str(single_user[0]).strip(), single_user[1].strip()))
            
        elif how_many_items == 1: 
            discord_user_list.append((str(row),str(single_user[0]).strip(), ''))
        elif how_many_items == 0:
            discord_user_list.append((str(row), '', ''))

        return discord_user_list
        

    def process_file_content(self,content):
        text_rows = [row.strip() for row in content.split('\n') if row != '']
        counter = 0
        list_teams = []

        for index, single_row in enumerate(text_rows):
            if '##' in single_row: ## Sprawdzic czy ##A ## C / zadziala
                if self.main_thread_description == '':
                    self.main_thread_description = "".join(str(x) + '\n' for x in text_rows[text_rows.index('***')+1 : index])
                
                list_teams.append(Team(str(single_row.split('##')[1])))
                if len(list_teams) != 1:
                    counter = counter+1
            else:
                stripped_row = single_row.replace('\\', '').strip()  # Usuwamy białe znaki na początku i końcu wiersza
                match = pattern.match(stripped_row)  # Dopasowujemy tylko raz
                if match:
                    number_before_dot = match.group(1)  # Wyciągamy liczbę przed kropką
                    user_nick_list = stripped_row.split(str(number_before_dot)+'.')[1]
                    if user_nick_list != '':
                        list_teams[counter].users_list.append(self.get_discord_user_list(number_before_dot,user_nick_list))
                    else:
                        list_teams[counter].users_list.append((str(number_before_dot)+'.', ''))
        return list_teams

            # elif self.pattern.match(single_row.strip()) and main_thread_description != '':
            #     print('mleko')
            #     number_before_dot = self.pattern.match.group(1)  # Wyciągamy liczbę przed kropką
            #     print(f"Wiersz zaczyna się od liczby {number_before_dot} z kropką: {number_before_dot}")


            # if ('1.' or '2.') in single_row and main_thread_description != '': # To znaczy ze jestesmy przy liscie
            #     list_mode = True
            #     print('lisra')
                # Trzeba:
                # sprawdzic czy cos w niej jest 
                # Utworzyc usera i dodac go do teamu / pamiętać o sprawdzeniu member
                ## Dodac opis do teamu
               # list_teams[counter].description = 'test'
            # elif list_mode: # A co jak zacznie sie od '2. '
            #     try:
            #         if '.' in single_row:
            #             print('Row with user lets assign them')
            #             # A co jakby to była tupla z userami [Pozycja , Nick]

            #         print('mleko')

            #     except Exception as e:
            #         pass
        # for index, single_row in enumerate(text_rows):
        #     if thread_author_name == '' and 'Created by' in single_row:
        #         try:
        #             thread_author_name = single_row.split('Created by')[1]
        #             createdby_included = True
        #         except Exception as e:
        #             pass
        #     elif table_start_index == 0 and 'Comp:' in single_row:
        #         table_start_index = index+1
        # if createdby_included:
        #     thread_description = text_rows[1:table_start_index-1]
        #     only_name = thread_author_name.strip()

        #     nickName = ctx.guild.get_member_named(only_name)
        #     if nickName != None:
        #         thread_author_name= nickName.mention
        #         thread_author = nickName
        #     else:
        #         thread_author_name = '<@969918981660086342>'

        # else:
        #     thread_description = thread_description.join(text_rows[0:table_start_index-1])  
        #     thread_author_name = '<@969918981660086342>' 

        # if '10.' in text_rows[-1]: 
        #     thread_name= 'Thread_' + str(random.randint(0, 1000))
        #     for single_row in text_rows[table_start_index:]:
        #         nicks_list_prep = single_row.split('.')[1].strip().split(',')
        #         rows_nick_list.append(nicks_list_prep)
        # else:
        #     thread_name = text_rows[-1].strip()
        #     for single_row in text_rows[table_start_index:-1]:
        #         nicks_list_prep = single_row.split('.')[1].strip().split(',')
        #         rows_nick_list.append(nicks_list_prep)

        # discord_user_list = get_discord_user_list(ctx.guild,rows_nick_list)

        # thread_desc = file_description_template.format(
        #     thread_author = thread_author_name,
        #     description = ''.join(thread_description),
        #     first_row= ','.join(discord_user_list[0]) if discord_user_list[0][0] != '' and discord_user_list[0][0] != None else '',
        #     second_row= ','.join(discord_user_list[1]) if discord_user_list[1][0] != '' and discord_user_list[1][0] != None else '',
        #     third_row= ','.join(discord_user_list[2]) if discord_user_list[2][0] != '' and discord_user_list[2][0] != None else '',
        #     fourth_row=','.join(discord_user_list[3]) if discord_user_list[3][0] != '' and discord_user_list[3][0] != None else '',
        #     fifth_row=','.join(discord_user_list[4]) if discord_user_list[4][0] != '' and discord_user_list[4][0] != None else '',
        #     sixth_row=','.join(discord_user_list[5]) if discord_user_list[5][0] != '' and discord_user_list[5][0] != None else '',
        #     seventh_row=','.join(discord_user_list[6]) if discord_user_list[6][0] != '' and discord_user_list[6][0] != None else '',
        #     eighth_row=','.join(discord_user_list[7]) if discord_user_list[7][0] != '' and discord_user_list[7][0] != None else '',
        #     ninth_row=','.join(discord_user_list[8]) if discord_user_list[8][0] !='' and discord_user_list[8][0] != None else '',
        #     tenth_row=','.join(discord_user_list[9]) if discord_user_list[9][0] != '' and discord_user_list[9][0] != None else '',
        # )
        # initial_message = await ctx.channel.send(thread_desc or "No description provided.")
        # thread = await initial_message.create_thread(name=thread_name, auto_archive_duration=thread_lifetime) 

    def add_author(self, Nick = ''):
        print('mleko')
        self.thread_author = Nick
        return self
    

    def add_user(self,message,author):
        if len(self.teams) == 0:
            return self

        if len(self.teams) > 1:
            devided_message = message.split(' ')
            team_index = devided_message[1].replace('pt','')
            postion_index = devided_message[2]

        else:
            devided_message = message.split(' ')
            team_index = '1'
            postion_index = devided_message[1]

        users_list = self.teams[int(team_index) - 1].users_list

        for index ,place_holder in  enumerate(users_list):
            if isinstance(place_holder, list):
                #if place_holder[0] == postion_index+'.' and place_holder[2] == '':
                place_holder = list(place_holder[0])
                if place_holder[0] == postion_index and place_holder[2] == '':
                    place_holder[2] = author.mention
                    users_list[index] = place_holder
            elif isinstance(place_holder, tuple):
                if place_holder[0] == postion_index+'.' and place_holder[1] == '':
                    place_holder = list(place_holder) 
                    place_holder.append(author.mention)
                    users_list[index] = place_holder




            



        return self
    
    def delete_user(self):
        print('innego')
        return self
    
    def show_users_in_description(self):
        self.users_in_description = True
        return self

    def build_description(self):
        final_text = '*** \n'
        if 'Call started by ' not in  self.main_thread_description:
            final_text += 'Call started by ' + self.thread_author + ' \n'

        final_text += self.main_thread_description

        for team in self.teams:
            final_text += ' \n '
            final_text += '##' + str(team.name) + ' \n '
            for row in team.users_list:
                if isinstance(row, list):
                    if len(row) == 1:
                        row = list(row[0])
                    if self.users_in_description and row[2] != '':
                        if row[0].endswith('.'):
                            row[0] = row[0].replace('.','')
                            print('mleko')
                        temp_testcik = str(row[0]) + '\\.' + row[1] + ' -' + row[2] + ' \n '
                        final_text += temp_testcik
                    else:
                        temp_text = str(row[0]) + '\. ' + row[1] + ' \n '
                        final_text += temp_text
                elif isinstance(row, tuple):
                    temp = row[1]
                    temp_text = str(row[0]) + temp  + '\n '
                    final_text += temp_text
        return final_text
    



    
class Team:
    def __init__(self, name = ''):
        self.name = name
        self.description = ''
        self.users_list = []
