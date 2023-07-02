from colored import attr, fg
from ui import Center, Colors, Colorate


#! Colored code
yellow = fg("yellow")
white = fg("white")
blue = fg(20)
blues = fg(27)
cyan = fg('cyan')
green = fg(46)
r124 = fg(124)
red = fg('red')
purple = fg("purple_1a")
grey = fg("grey_27")
org = fg('orange_red_1')
bold = attr("bold")
reset = attr("reset")


title = r'''
 ▀█▀ ██▀ █▄ ▄█ █▀▄ █▄ ▄█ ▄▀▄ █ █
  █  █▄▄ █ ▀ █ █▀  █ ▀ █ █▀█ █ █▄▄ ▄
'''
txt = r'BY: ══ᵂʰᵒᴬᴹ!'
bann = (Colorate.Diagonal(Colors.red_to_yellow, Center.XCenter(title)))
text = (Colorate.Horizontal(Colors.black_to_white, Center.XCenter(txt)))

logo = f'''
{bann}
    {text}
'''
strg = f'{grey}{"»" * 70}{reset}'

empty = f'{red}{bold}Your Mailbox is empty!{reset}'
checkinput = f'{red}{bold}Check your input!{reset}'
selectoption = f'{green}Please select your option: {reset}'
remtxt = f'{yellow}Text file has been removed!{reset}'

generator = f'''
{purple}{bold}[1] {reset}{blue}{bold}Generate With Random Email{reset}
{purple}{bold}[2] {reset}{blue}{bold}Generate With Custom Email{reset}
{purple}{bold}[3] {reset}{blue}{bold}Check Inbox With Existing Email{reset}
{purple}{bold}[4] {reset}{blue}{bold}Delete Email From Server{reset}
{purple}{bold}[5] {reset}{blue}{bold}Exit Program{reset}
'''

deletemail = f'''
{purple}{bold}[1] {reset}{blue}{bold}Delete Manually{reset}
{purple}{bold}[2] {reset}{blue}{bold}Delete All in TXT File{reset}
'''

custemail = f'''
{purple}{bold}[1] {reset}{blue}{bold}Random Username{reset}
{purple}{bold}[2] {reset}{blue}{bold}Custom Username{reset}
'''

custdom = f'{green}Do you want to custom domain? Y|N{reset}'
