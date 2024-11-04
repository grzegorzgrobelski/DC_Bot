import re
import random
pattern = re.compile(r"^([1-9][0-9]?)\.")

class FileManager:
    def __init__(self,guild, content, is_on_init = False):
        self.main_thread_description = ''
        self.file_content = content
        self.thread_name = ''
        self.thread_author = ''
        self.guild = guild
        self.users_in_description = False
        self.is_on_init = is_on_init
        self.teams = self.process_file_content(self.file_content)
        

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
        come_from_file = False
        if '***' in content:
            come_from_file = True



        for index, single_row in enumerate(text_rows):
            if '##' in single_row: ## Sprawdzic czy ##A ## C / zadziala
                if self.main_thread_description == '' and come_from_file:
                    self.main_thread_description = "".join(str(x) + '\n' for x in text_rows[text_rows.index('***')+1 : index])
                elif self.main_thread_description == '' and not come_from_file:
                    self.main_thread_description = "".join(str(x) + '\n' for x in text_rows[: index])


                
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
                elif self.is_on_init and self.thread_name == '' and '==' in single_row.strip():
                    self.thread_name = str(single_row.strip().split('==')[1])
        
        return list_teams

          
    def add_author(self, Nick = ''):
        self.thread_author = Nick
        return self
    
    def add_user(self,message,author):
        if len(self.teams) == 0:
            return self

        if len(self.teams) > 1:
            devided_message = message.split(' ')
            team_index = devided_message[1].replace('pt','')
            try:
                postion_index = devided_message[2]
            except Exception as e:
                print(e)
                print('User probably used the wrong command')

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
                    self.delete_user(author)
                    place_holder[2] = author.mention
                    users_list[index] = place_holder
                    return

            elif isinstance(place_holder, tuple):
                if place_holder[0] == postion_index+'.' and place_holder[1] == '':

                    self.delete_user(author)

                    place_holder = list(place_holder) 
                    place_holder.append(author.mention)
                    users_list[index] = place_holder
                    break




            



        return self
    
    def delete_user(self, author):
        #users_list = self.teams[int(team_index) - 1].users_list
        for team in self.teams:
            for index ,place_holder in  enumerate(team.users_list):
                if isinstance(place_holder, list):
                    #if place_holder[0] == postion_index+'.' and place_holder[2] == '':
                    place_holder_list = list(place_holder[0])
                    if place_holder_list[2] == author.mention:
                        place_holder_list[2] = ''
                        team.users_list[index] = place_holder_list
                        break
                elif isinstance(place_holder, tuple):
                    if place_holder[1] == author.mention:
                        place_holder = list(place_holder) 
                        place_holder.append('')
                        team.users_list[index] = place_holder
                        break

        return self
    
    def show_users_in_description(self):
        self.users_in_description = True
        return self

    def build_description(self):
        #final_text = '*** \n'
        final_text = ''
        if 'Call started by ' not in  self.main_thread_description:
            final_text += 'Call started by ' + self.thread_author + '\n'

        final_text += self.main_thread_description 
        
        #final_text += 
        for team in self.teams:
            final_text += '\n' + '## ' + str(team.name) + '\n '
            for row in team.users_list:
                if isinstance(row, list):
                    if len(row) == 1:
                        row = list(row[0])
                    if self.users_in_description and row[2] != '':
                        if row[0].endswith('.'):
                            row[0] = row[0].replace('.','')
                        temp_testcik = str(row[0]) + '\\. ' + row[1] + ' -' + row[2] + ' \n '
                        final_text += temp_testcik
                    else:
                        temp_text = str(row[0]) + '\. ' + row[1] + ' \n '
                        final_text += temp_text
                elif isinstance(row, tuple):
                    temp = row[1]
                    temp_text = str(row[0]) + temp  + '\n '
                    final_text += temp_text
        return final_text
    
    def get_thread_name(self, message_content):
        if message_content != '':
            return message_content
        if self.thread_name != '':
            return self.thread_name
        return 'Sign up in the thread ' + str(random.randint(0, 1000))


    
class Team:
    def __init__(self, name = ''):
        self.name = name
        self.description = ''
        self.users_list = []
