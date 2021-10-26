import requests
import json
import random
import time
import sys

bridge_ip = "192.168.178.24"
bridge_username = "ywaV8pN1EWbGOpjNzfe0DvSTJhe8eiHhWZUJo4vV"


alphabet = "abcdefghijklmnopqrstuvwxyz"
groups = { "wohnzimmer": "4", "schlafzimmer" : "1" } # change to other number if different area
    


"""legend
    0 normal
	1 FLICKER (first variety)
	2 SLOW STRONG PULSE
	3 CANDLE (first variety)
	4 FAST STROBE
	5 GENTLE PULSE 1
	6 FLICKER (second variety)
	7 CANDLE (second variety)
	8 CANDLE (third variety)
	9 SLOW STROBE (fourth variety)
	10 FLUORESCENT FLICKER
	11 SLOW PULSE NOT FADE TO BLACK
"""
lamp_style = {  0: "m",
                1: "mmnmmommommnonmmonqnmmo",
                2: "abcdefghijklmnopqrstuvwxyzyxwvutsrqponmlkjihgfedcba",
                3: "mmmmmaaaaammmmmaaaaaabcdefgabcdefg",
                4: "mamamamamama",
                5: "jklmnopqrstuvwxyzyxwvutsrqponmlkj",
                6: "nmonqnmomnmomomno",
                7: "mmmaaaabcdefgmmmmaaaammmaamm",
                8: "mmmaaammmaaammmabcdefaaaammmmabcdefmmmaaaa",
                9: "aaaaaaaazzzzzzzz",
                10: "mmamammmmammamamaaamammma",
                11: "abcdefghijklmnopqrrqponmlkjihgfedcba"
    }



def turn_on_group(where, groups=groups):
    group_id = groups[where]

    payload = {"on":True}
    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    #print(r)



def turn_off_group(where, groups=groups):
    group_id = groups[where]

    payload = {"on":False}
    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    #print(r)



def rgb_color_group(where, groups=groups, color=""):
    group_id = groups[where]
    rgb = str(color).split(";")

    X = float(rgb[0]) * 0.649926 + float(rgb[1]) * 0.103455 + float(rgb[2]) * 0.197109
    Y = float(rgb[0]) * 0.234327 + float(rgb[1]) * 0.743075 + float(rgb[2]) * 0.022598
    Z = float(rgb[0]) * 0.0000000 + float(rgb[1]) * 0.053077 + float(rgb[2]) * 1.035763

    try:
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
    except:
        x = 1
        y = 1

    payload = {"xy": [x, y]}
    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    




def color_group(where, groups=groups, color_id=0):
    group_id = groups[where]

    xy_value = map(float, str(color_id).split(";"))

    #print("DEBUG::", xy_value)
    try:
        color_number = int(color_id)
    except:
        color_number = 0


    #if color_number > 65536:
    #    color_number = 65535
    #elif color_number < 0:
    #    color_number = 0


    payload = {"xy":list(xy_value)}
    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    #print(r)




def brightness_group(where, groups, brightnesID):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    len_alpha = len(alphabet)

    group_id = groups[where]
    
    brightness_density = int(int(alphabet.find(brightnesID)) * (255/(len_alpha-1)))

    if brightness_density < 0:
        brightness_density = 0
    elif brightness_density >= 254:
        brightness_density = 255


    payload = {"bri":brightness_density}
    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    #print(r)




def saturation_group(where, groups, brightnesID):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    len_alpha = len(alphabet)

    group_id = groups[where]
    
    brightness_density = int(int(alphabet.find(brightnesID)) * (255/(len_alpha-1)))

    if brightness_density < 0:
        brightness_density = 0
    elif brightness_density >= 254:
        brightness_density = 255


    payload = {"sat":brightness_density}
    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    #print(r)



def crazy_multicall(where, groups, saturation_density, brightness_density, rgb):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    len_alpha = len(alphabet)

    group_id = groups[where]
    
    brightness_density = int(int(alphabet.find(brightness_density)) * (255/(len_alpha-1)))
    saturation_density = int(int(alphabet.find(saturation_density)) * (255/(len_alpha-1)))

    if brightness_density < 0:
        brightness_density = 0
    elif brightness_density >= 254:
        brightness_density = 255

    if saturation_density < 0:
        saturation_density = 0
    elif saturation_density >= 254:
        saturation_density = 255


    rgb = str(rgb).split(";")

    X = float(rgb[0]) * 0.649926 + float(rgb[1]) * 0.103455 + float(rgb[2]) * 0.197109
    Y = float(rgb[0]) * 0.234327 + float(rgb[1]) * 0.743075 + float(rgb[2]) * 0.022598
    Z = float(rgb[0]) * 0.0000000 + float(rgb[1]) * 0.053077 + float(rgb[2]) * 1.035763

    try:
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
    except:
        x = 1
        y = 1

    payload = {"sat":saturation_density,
               "bri":brightness_density,
               "xy":[x,y]}

    #print("DEBUG::", payload)

    headers = {'content-type': 'application/json'}
    r = requests.put("http://"+bridge_ip+"/api/"+bridge_username+"/groups/"+str(group_id)+"/action", data=json.dumps(payload), headers=headers)
    #print(r)





def test_brightness(area="wohnzimmer"):
    try:
        for letter in alphabet:
            brightness_group(where=area, groups=groups, brightnesID=letter)
            time.sleep(1)
        

    except Exception as master_error:
        print("sth. went horrible wrong with code: " + str(master_error))



def test_brightness_specific(my_letter="", area="wohnzimmer"):
    try:
        if my_letter in alphabet:
            brightness_group(where=area, groups=groups, brightnesID=my_letter)
        else:
            print("cant test with: " + my_letter)
        

    except Exception as master_error:
        print("sth. went horrible wrong with code: " + str(master_error))



def test_saturation_specific(my_letter="", area="wohnzimmer"):
    try:
        if my_letter in alphabet:
            saturation_group(where=area, groups=groups, brightnesID=my_letter)
        else:
            print("cant test with: " + my_letter)
        

    except Exception as master_error:
        print("sth. went horrible wrong with code: " + str(master_error))



def test_color(my_color="", area="wohnzimmer", style="single"):
    if style == "single":
        try:
            color_group(where=area, groups=groups, color_id=my_color)

        except Exception as master_error:
            print("sth. went horrible wrong with code: " + str(master_error))
    elif style == "rgb":
        try:
            rgb_color_group(where=area, groups=groups, color=my_color)

        except Exception as master_error:
            print("sth. went horrible wrong with code: " + str(master_error))
    


#######################
# cool program stuff 
#######################
def start_halloween_spectacle(my_program, area="wohnzimmer"):
    try:
        while(True):
            for letter in lamp_style[int(my_program)]:
                brightness_group(where=area, groups=groups, brightnesID=letter)
                time.sleep(0.3)


    except Exception as master_error:
        print("sth. went horrible wrong with code: " + str(master_error))




def halloween_2_0(area="wohnzimmer"):
    try:
        while(True):
            r_val = random.randint(1,255)
            g_val = random.randint(1,255)
            b_val = random.randint(1,255)

            bright_val = random.randint(0, len(alphabet)-1)
            sat_val = random.randint(0,len(alphabet)-1)

            rgb_text = str(r_val) + ";" + str(g_val) + ";" + str(b_val)
            """            test_color(my_color = rgb_text, area= area, style="rgb")
            test_brightness_specific(my_letter=alphabet[bright_val], area=area)
            test_saturation_specific(my_letter=alphabet[sat_val], area=area)
            """
            crazy_multicall(where=area, groups=groups, saturation_density=alphabet[sat_val], brightness_density=alphabet[bright_val], rgb=str(rgb_text))

            time.sleep(2)
    except Exception as err:
        print("error" + str(err)) 




# function calls: 
#   python test_hue_script.py run halloween2 wohnzimmer
#   python test_hue_script.py run halloween1 10 wohnzimmer
#   python test_hue_script.py test brightness_all wohnzimmer
#   python test_hue_script.py test brightness_specific a wohnzimmer
#   python test_hue_script.py test saturation_specifc h wohnzimmer
#   python test_hue_script.py test color 0.023;0.456 wohnzimmer
#   python test_hue_script.py test rgbcolor 255;0;255 wohnzimmer
#   python test_hue_script.py debug off schlafzimmer
#   python test_hue_script.py debug on schlafzimmer
# abort the script with strg+c



# hue - living room 9231, xy [0.4128; 0.3953]
if __name__ == "__main__":
    print("if u using arguments use program_name style program keyword")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test" and len(sys.argv) >= 4:
            print("test")
            try:
                if sys.argv[2] == "brightness_all":
                    test_brightness(area = str(sys.argv[3]))
                elif sys.argv[2] == "brightness_specific":
                    test_brightness_specific(my_letter = str(sys.argv[3]), area= str(sys.argv[4]))
                elif sys.argv[2] == "saturation_specific":
                    test_saturation_specific(my_letter = str(sys.argv[3]), area= str(sys.argv[4]))
                elif sys.argv[2] == "color":
                    test_color(my_color = sys.argv[3], area= str(sys.argv[4]), style="single")
                elif sys.argv[2] == "rgbcolor":
                    test_color(my_color = sys.argv[3], area= str(sys.argv[4]), style="rgb")
                else:
                    print("nothing to do")
                    print("possible tests are: brightness_all, brightness_specific")
            except Exception as argument_error:
                print("to less arguments test need 3 or 4 arguments")    


        elif sys.argv[1] == "debug" and len(sys.argv) >= 4:
            try:
                print("debug")
                if sys.argv[2] == "on":
                    turn_on_group(where=sys.argv[3])
                elif sys.argv[2] == "off":
                    turn_off_group(where=sys.argv[3])
                else:
                    print("nothing to do")
                    print("possible: on or off")

            except Exception as debug_arguments:
                print("use debug specific arguments as 3rd argument" + str(debug_arguments))
        elif sys.argv[1] == "run":
            if sys.argv[2] == "halloween1":
                if str(sys.argv[3]).isnumeric():
                    print("halloween spectacle - abort script with strg+c")
                    my_program = int(sys.argv[3])
                    start_halloween_spectacle(my_program, area=sys.argv[4])
                else:
                    print("dont know what to do")
            elif sys.argv[2] == "halloween2":
                    halloween_2_0(area=sys.argv[3])
                

    else:
        print("use test, debug or a number as second argument")



    #my_program = 10

    # start_halloween_spectacle(my_program)