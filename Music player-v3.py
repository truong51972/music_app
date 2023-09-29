import pygame
import os
import pygame
import subprocess
import sys
from random import randint
from pygame.constants import KEYDOWN, KEYUP, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP
pygame.init()
from pygame import mixer
mixer.init()

LOCATION_FILE = os.getcwd()

class Music:
    def __init__(self, name, singer, directory) :
        self.name = name
        self.singer = singer
        self.directory = directory
        
class Music_action:
    def __init__(self, list_music):
        self.list_music = list_music

        previous_information = self.get_random_music_form_list()
        while True:
            current_information = self.get_random_music_form_list()
            if previous_information[0] != current_information[0]:
                break
        while True:
            next_information = self.get_random_music_form_list()
            if current_information[0] != next_information[0]:
                break
        self.list_information_music = [previous_information, current_information, next_information]
        self.current_music = (self.list_information_music[1])[2]
        self.location_file_data = LOCATION_FILE + "\\music\\"

    def convert(self,string):
        out = ""
        in_list_lower = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
        outlist_lower = "aaaaaaaaaaaaaaaaaoooooooooooooooooeeeeeeeeeeeuuuuuuuuuuuiiiiiyyyyyd"
        in_list_upper = in_list_lower.upper()
        outlist_upper = outlist_lower.upper()
        for i in range(len(string)):
            if string[i] in in_list_lower:
                out += outlist_lower[in_list_lower.find(string[i])]
            elif string[i] in in_list_upper:
                out += outlist_upper[in_list_upper.find(string[i])]
            else:
                out += string[i] 
        return out
        # return string

    def get_time_end(self):
        location_file_file = self.location_file_data + self.current_music
        location_file_music = location_file_file.rstrip()
        time_end = pygame.mixer.Sound(location_file_music).get_length()
        return time_end*1000

    def get_pos_time(self):
        return pygame.mixer.music.get_pos()

    def set_pos_time(self,time):
        pygame.mixer.music.set_pos(time)

    def get_random_music_form_list(self):
        list_music = self.list_music
        random = randint(0,len(list_music)) - 1
        name = self.convert(list_music[random].name)
        singer = self.convert(list_music[random].singer)
        directory = list_music[random].directory
        list_return = [name, singer, directory]
        return list_return

    def play_music(self):
        pygame.mixer.music.pause()
        location_file_music = self.location_file_data + self.current_music
        location_file_music = location_file_music.rstrip()
        pygame.mixer.music.load(location_file_music)
        pygame.mixer.music.play(0)
        pygame.mixer.music.unpause()

    def next(self):
        self.list_information_music[0] = self.list_information_music[1]
        self.list_information_music[1] = self.list_information_music[2]
        while True:
            self.list_information_music[2] = self.get_random_music_form_list()
            if (self.list_information_music[2])[0] != (self.list_information_music[1])[0]:
                break
        self.current_music = (self.list_information_music[1])[2]
        self.play_music()
    
    def previous(self):
        self.list_information_music[2] = self.list_information_music[1]
        self.list_information_music[1] = self.list_information_music[0]
        while True:
            self.list_information_music[0] = self.get_random_music_form_list()
            if (self.list_information_music[0])[0] != (self.list_information_music[1])[0]:
                break
        self.current_music = (self.list_information_music[1])[2]
        self.play_music()

    def stop(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

def get_list_to_txt():
    location_file_data = LOCATION_FILE + "\music"
    subprocess.Popen(['powershell.exe', 'dir "{0}" -Name > mp3_data.txt'.format(location_file_data)], stdout=sys.stdout)

def music_file_name_process(music_file_name):
    music_file_name_processed = music_file_name.replace(".mp3","")
    music_file_name_processed = music_file_name_processed.rstrip()
    element = music_file_name_processed.split("-")
    name = element[0].strip()
    singer = element[1].strip()
    music_information = Music(name, singer, music_file_name)
    return music_information

def read_music_form_txt():
    list_music = []
    with open("mp3_data.txt", mode="r", encoding="utf-16") as file:
        while True:
            read_inforation = file.readline()
            if read_inforation == "":
                break
            music_information = music_file_name_process(read_inforation)
            list_music.append(music_information)                    
    return list_music

def check_in_rect(mouse_x, mouse_y, pos_x, pos_y, width, height):
    if (mouse_x in range(pos_x,pos_x+width) ) and (mouse_y in range(pos_y,pos_y+height) ):
        return True
    return False

def in_range(variable, min, max):
    if variable > max:
        variable = max
    elif variable < min:
        variable = min
    return variable

def convert_millisecond_to_hour(millisecond):
    second = int(millisecond/1000)
    minute = 0
    hour = 0
    while second >= 60:
        if second >=60:
            second -= 60
            minute += 1
        if minute >=60:
            minute -= 60
            hour += 1
    return hour, minute, second

def time_show(hour, minute, second):
    time = ""
    if hour <= 9:
        time += "0{0}:".format(hour)
    else:
        time += "{0}:".format(hour)
    if minute <= 9:
        time += "0{0}:".format(minute)
    else:
        time += "{0}:".format(minute)
    if second <= 9:
        time += "0{0}".format(second)
    else:
        time += "{0}".format(second)
    return time

def get_middle(width, width_text):
    return (width/2 - width_text/2)

def text_render(list_information_music):
    font = 'time new roman'
    color = (255,255,255)
    font_current_name = pygame.font.SysFont(font, 30)
    font_current_singer = pygame.font.SysFont(font, 23)
    font_previous_next_name = pygame.font.SysFont(font, 20)
    font_previous_next_singer = pygame.font.SysFont(font, 15)
    previous_information, current_information, next_information = list_information_music
    previous_name = previous_information[0]
    previous_singer = previous_information[1]
    current_name = current_information[0]
    current_singer = current_information[1]
    next_name = next_information[0]
    next_singer = next_information[1]
    text_previous_name = font_previous_next_name.render(previous_name, True, color)
    text_previous_singer = font_previous_next_singer.render(previous_singer, True, color)
    text_current_name = font_current_name.render(current_name, True, color)
    text_current_singer = font_current_singer.render(current_singer, True, color)
    text_next_name = font_previous_next_name.render(next_name, True, color)
    text_next_singer = font_previous_next_singer.render(next_singer, True, color)
    list_return = (text_previous_name, text_previous_singer, text_current_name, text_current_singer, text_next_name, text_next_singer)
    return  list_return

def play_point(time_pos, time_end, start, end):
    a = time_pos / time_end
    b = end - start
    point = int(start + (a * b))
    return point

def set_point(point, time_end, start, end):
    a = end - start
    b = (point - start) / a 
    time = b * time_end
    return time

def main():
    WIDTH = 400
    HEIGHT = 300
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Mp3 Music player')
    running = True
    clock = pygame.time.Clock()
    location_file_data = LOCATION_FILE + "\\image"
    icon = pygame.image.load (location_file_data + '\\icon_music.png')
    pygame.display.set_icon(icon)
    play_icon_red = pygame.image.load(location_file_data + '\\play_icon_red.png')
    play_icon_blue = pygame.image.load(location_file_data + '\\play_icon_blue.png')
    stop_icon_red = pygame.image.load(location_file_data + '\\stop_icon_red.png')
    stop_icon_blue = pygame.image.load(location_file_data + '\\stop_icon_blue.png')
    next_icon_red = pygame.image.load(location_file_data + '\\next_icon_red.png')
    next_icon_blue = pygame.image.load(location_file_data + '\\next_icon_blue.png')
    previous_icon_red = pygame.image.load(location_file_data + '\\previous_icon_red.png')
    previous_icon_blue = pygame.image.load(location_file_data + '\\previous_icon_blue.png')
    background = pygame.image.load(location_file_data + '\\background_music.png')
    box_line = pygame.image.load(location_file_data + '\\box_line.png')
    volume_0 = pygame.image.load(location_file_data + '\\volume 0.png')
    volume_1 = pygame.image.load(location_file_data + '\\volume 1.png')
    volume_2 = pygame.image.load(location_file_data + '\\volume 2.png')
    volume_3 = pygame.image.load(location_file_data + '\\volume 3.png')
    
    get_list_to_txt()
    list_music = read_music_form_txt()
    
    color_text = (255,255,255)

    font_time = pygame.font.SysFont('time new roman', 20)

    volume = 0.5
    volume_up = False
    volume_down = False
    music_action = Music_action(list_music)

    play_checker = True
    key_space_checker = False
    key_next_checker = False
    key_previous_checker = False
    key_next_checker_1 = 0
    key_next_checker_2 = 1
    key_previous_checker_1 = 0
    key_previous_checker_2 = 1
    in_time_line = False
    time_set = 0
    time_played = 0 

    music_action.play_music()
    time_end = music_action.get_time_end()
    while running:		
        clock.tick(30)
        mouse_x, mouse_y = pygame.mouse.get_pos()	
        screen.blit(background,(0,0))
        screen.blit(box_line , (100, 239))
       
        list_information = text_render(music_action.list_information_music)

        pygame.display.set_caption(music_action.current_music)

        screen.blit(list_information[0],(get_middle(WIDTH, (list_information[0].get_rect())[2]),55))
        screen.blit(list_information[1],(get_middle(WIDTH, (list_information[1].get_rect())[2]),70))
        pygame.draw.line(screen,(255,255,255),(75,87),(325,87),2)
        screen.blit(list_information[2],(get_middle(WIDTH, (list_information[2].get_rect())[2]),105))
        screen.blit(list_information[3],(get_middle(WIDTH, (list_information[3].get_rect())[2]),125))
        pygame.draw.line(screen,(255,255,255),(75,156),(325,156),2)
        screen.blit(list_information[4],(get_middle(WIDTH, (list_information[4].get_rect())[2]),164))
        screen.blit(list_information[5],(get_middle(WIDTH, (list_information[5].get_rect())[2]),179))

        MUSIC_END = pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(MUSIC_END)

        time_pos = music_action.get_pos_time() + time_set - time_played

        hour_pos, minute_pos, second_pos = convert_millisecond_to_hour(time_pos)
        hour_end, minute_end, second_end = convert_millisecond_to_hour(time_end)
        time_pos_show = "Time:" + time_show(hour_pos, minute_pos, second_pos)
        time_end_show = "End:" + time_show(hour_end, minute_end, second_end)
        text_time_pos = font_time.render(time_pos_show, True, color_text)
        text_time_end = font_time.render(time_end_show, True, color_text)
        screen.blit(text_time_pos,(10,205))
        screen.blit(text_time_end,(300,205))
        pygame.draw.line(screen,(0,0,0),(75,225),(325,225),3)
        pygame.mixer.music.set_volume(volume)
        
        if in_time_line:
            time_set = set_point(in_range(mouse_x,75,325),time_end,75,325)
            pygame.draw.circle(screen,(255,255,255),(in_range(mouse_x,75,325),225),6)
            music_action.set_pos_time(time_set/1000)
            time_played = music_action.get_pos_time()
        else:
            pygame.draw.circle(screen,(255,255,255),(play_point(time_pos,time_end,75,325),225),6)

        if play_checker == False:
            music_action.stop()
        else:
            music_action.resume()

        if check_in_rect(mouse_x, mouse_y, 175, 240, 50, 50) or key_space_checker:
            if play_checker:
                screen.blit(stop_icon_red , (175, 240))
            else:
                screen.blit(play_icon_red , (175, 240))       
        else:
            if play_checker:
                screen.blit(stop_icon_blue , (175, 240))
            else:
                screen.blit(play_icon_blue , (175, 240))
        
        if volume >= 2/3:
            screen.blit(volume_3,(330,255))
        elif volume >= 1/3:
            screen.blit(volume_2,(330,255))
        elif volume > 0:
            screen.blit(volume_1,(330,255))
        elif volume == 0:
            screen.blit(volume_0,(330,255))
        
        present_volume = str(volume*100) + "%"
        present_volume = font_time.render((str(int(volume*100)) + "%"), True, color_text)
        screen.blit(present_volume,(355,259))

        if volume_up:
            volume += 0.01
            volume = in_range(volume,0,1)
            # volume = round(volume,2)
        if volume_down:
            volume -= 0.01
            volume = in_range(volume,0,1)
            # volume = round(volume,2)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if check_in_rect(mouse_x, mouse_y, 330, 255, 60, 20):
                        volume += 0.05
                        volume = in_range(volume,0,1)
                        # volume = round(volume,2)
                if event.button == 5:
                    if check_in_rect(mouse_x, mouse_y, 330, 255, 60, 20):
                        volume -= 0.05
                        volume = in_range(volume,0,1)
                        # volume = round(volume,2)
                if event.button == 1:
                    if check_in_rect(mouse_x, mouse_y, 175, 240, 50, 50):
                        play_checker = not play_checker
                    if check_in_rect(mouse_x, mouse_y, 260, 250, 30, 30):
                        key_next_checker_1 += 1
                    if check_in_rect(mouse_x, mouse_y, 110, 250, 30, 30):
                        key_previous_checker_1 += 1

                    if check_in_rect(mouse_x, mouse_y, 330, 255, 20, 20):
                        if volume != 0:
                            volume_temp = volume
                            volume = 0
                        else:
                            volume = volume_temp
                    if check_in_rect(mouse_x, mouse_y, 75, 221, 250, 11):
                        in_time_line = True
                        play_checker = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if in_time_line:
                        in_time_line = False
                        play_checker = True

            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    key_space_checker = True
                    play_checker = not play_checker
                elif event.key == K_RIGHT:
                    key_next_checker = True
                    key_next_checker_1 += 1
                elif event.key == K_LEFT:
                    key_previous_checker = True
                    key_previous_checker_1 += 1
                elif event.key == K_UP:
                    volume_up = True
                elif event.key == K_DOWN:
                    volume_down = True
                elif event.key ==  109:
                    if volume != 0:
                        volume_temp = volume
                        volume = 0
                    else:
                        volume = volume_temp

            if event.type == KEYUP:
                if event.key == K_SPACE:
                    key_space_checker = False
                if event.key == K_UP:
                    volume_up = False
                if event.key == K_DOWN:
                    volume_down = False
                if event.key == K_RIGHT:
                    key_next_checker = False
                if event.key == K_LEFT:
                    key_previous_checker = False
            if event.type == MUSIC_END:
                key_next_checker_1 += 1

        if check_in_rect(mouse_x, mouse_y, 260, 250, 30, 30) or key_next_checker:
            screen.blit(next_icon_red , (260, 250))
        else:
            screen.blit(next_icon_blue , (260, 250))

        if check_in_rect(mouse_x, mouse_y, 110, 250, 30, 30) or key_previous_checker:
            screen.blit(previous_icon_red , (110, 250))
        else:
            screen.blit(previous_icon_blue , (110, 250))
        
        pygame.display.flip()

        if key_previous_checker_1 == key_previous_checker_2:
            key_previous_checker_2 += 1
            music_action.previous()
            time_end = music_action.get_time_end()
            time_set = 0
            time_played = 0

        if key_next_checker_1 == key_next_checker_2:
            key_next_checker_2 += 1
            music_action.next()
            time_end = music_action.get_time_end()
            time_set = 0
            time_played = 0

    pygame.quit()

main()