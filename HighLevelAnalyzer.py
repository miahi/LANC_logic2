# Saleae Logic 2 High Level Analyzer for LANC video camera protocol
# Based on http://www.boehmel.de/lanc.htm
# First add an Async Serial analyzer with bit rate 9600 and standard settings

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, StringSetting, NumberSetting, ChoicesSetting
import struct

# command decoder  
c18 = {}
c18['00']='program 1'
c18['02']='program 2'
c18['04']='program 3'
c18['05']='mode (only HDV/AVCHD)'
c18['06']='program 4'
c18['08']='program 5'
c18['0A']='program 6'
c18['0C']='program 7'
c18['0E']='program 8'
c18['10']='program 9'
c18['12']='program 0 (10: SL-HF950 MKII)'
c18['14']='program 11 (SL-HF950 MKII)'
c18['16']='enter, program 12 (SL-HF950 MKII)'
c18['18']='program 13'
c18['1A']='program 14'
c18['1C']='program 15'
c18['1E']='program 16'
c18['20']='program +'
c18['22']='program -'
c18['24']=''
c18['26']=''
c18['28']='x2'
c18['2A']='mode movie/still (older models: power or viewfinder off)'
c18['2B']='photo write'
c18['2C']='eject'
c18['2E']='main/sub'
c18['30']='stop'
c18['32']='pause'
c18['33']='start/stop'
c18['34']='play'
c18['35']='tele (only CCD-V90)'
c18['36']='rew'
c18['37']='wide (only CCD-V90)'
c18['38']='fwd'
c18['39']='photo capture'
c18['3A']='rec'
c18['3C']='rec-pause (some devices)'
c18['3E']=''
c18['40']='still'
c18['42']=''
c18['44']='x1/10'
c18['46']='x1/5 (sometimes: vis. scan)'
c18['48']=''
c18['4A']='x14'
c18['4C']='x9'
c18['4E']='tracking auto/manual'
c18['50']='search -'
c18['52']='search +'
c18['54']='TV/VTR'
c18['56']=''
c18['58']=''
c18['5A']='VTR'
c18['5B']='date search / photo search / photo scan'
c18['5C']=''
c18['5E']='power off'
c18['60']='rev frame'
c18['62']='fwd frame'
c18['64']=''
c18['65']='edit-search -'
c18['66']='x1'
c18['67']='edit-search +'
c18['68']=''
c18['69']='rec-review (not i.e. TR-2200)'
c18['6A']=''
c18['6C']='sleep'
c18['6E']='tracking normal'
c18['70']=''
c18['72']=''
c18['74']='rew+play'
c18['76']=''
c18['78']='AUX'
c18['7A']='slow +'
c18['7B']='tape end search (HDV)'
c18['7C']='slow -'
c18['7E']=''
c18['80']=''
c18['82']='display mode'
c18['84']='menu up'
c18['86']='menu down'
c18['88']='tracking/fine +'
c18['8A']='tracking/fine -'
c18['8C']='counter reset'
c18['8E']='zero mem'
c18['90']='index mark'
c18['92']='index erase'
c18['94']='shuttle edit +'
c18['96']='shuttle edit -'
c18['98']='data code or goto'
c18['99']='data code or recording parameters'
c18['9A']='menu'
c18['9C']=''
c18['9E']='input select'
c18['A0']=''
c18['A2']='execute'
c18['A4']='quick timer'
c18['A6']='index'
c18['A8']=''
c18['AA']=''
c18['AC']='index search +, date search 01 (HDV)'
c18['AE']='index search -, date search -01 (HDV)'
c18['B0']='tape speed'
c18['B2']='goto zero / tape return (not DV)'
c18['B4']='counter display, data screen'
c18['B6']='open/close (SL-HF950), replay (FauHaEss)'
c18['B8']='timer display'
c18['BA']=''
c18['BC']=''
c18['BD']='date display off'
c18['BE']=''
c18['BF']='date display on'
c18['C0']='timer set'
c18['C2']='menu right, next'
c18['C4']='menu left'
c18['C6']='timer clear'
c18['C8']='timer check'
c18['CA']='timer record'
c18['CC']=''
c18['CE']=''
c18['D0']='audio dub'
c18['D2']=''
c18['D4']='edit assemble'
c18['D6']='edit mark'
c18['D8']='synchro edit'
c18['DA']=''
c18['DC']='digital off (VCR), print (DV)'
c18['DE']='speed +'
c18['E0']='speed -'
c18['E2']='stop motion'
c18['E4']=''
c18['E6']=''
c18['E8']='channel scan / flash motion'
c18['EA']=''
c18['EC']='voice boost'
c18['EE']=''
c18['F0']=''
c18['F2']=''
c18['F4']=''
c18['F6']=''
c18['F8']='digital scan'
c18['FA']='high-speed-rew'
c18['FC']='still/shuttle (EV-S880)'
c18['FE']=''

c28={}
c28['00']='zoom Tele: slowest speed'
c28['02']='zoom Tele: faster than 00'
c28['04']='zoom Tele: faster than 02'
c28['06']='zoom Tele: faster than 04'
c28['08']='zoom Tele: faster than 06'
c28['0A']='zoom Tele: faster than 08'
c28['0C']='zoom Tele: faster than 0A'
c28['0E']='zoom Tele: fastest speed'
c28['10']='zoom Wide: slowest speed'
c28['12']='zoom Wide: faster than 10'
c28['14']='zoom Wide: faster than 12'
c28['16']='zoom Wide: faster than 14'
c28['18']='zoom Wide: faster than 16'
c28['1A']='zoom Wide: faster than 18'
c28['1C']='zoom Wide: faster than 1A'
c28['1E']='zoom Wide: fastest speed'
c28['21']='grid (AVCHD)'
c28['25']='fader'
c28['27']='rec start (DV, some cameras)'
c28['29']='rec stop (DV, some cameras)'
c28['30']='zoom Tele (avoiding digital zoom, some cameras): slowest speed'
c28['32']='zoom Tele (avoiding digital zoom, some cameras): faster than 30'
c28['34']='zoom Tele (avoiding digital zoom, some cameras): faster than 32'
c28['35']='Zoom Tele slow (working all cameras since approx. 1996)'
c28['36']='zoom Tele (avoiding digital zoom, some cameras): faster than 34'
c28['37']='Zoom Wide slow (working all cameras since approx. 1996)'
c28['38']='zoom Tele (avoiding digital zoom, some cameras): faster than 36'
c28['39']='Zoom Tele fast (working all cameras since approx. 1996)'
c28['3A']='zoom Tele (avoiding digital zoom, some cameras): faster than 38'
c28['3B']='Zoom Wide fast (working all cameras since approx. 1996)'
c28['3C']='zoom Tele (avoiding digital zoom, some cameras): faster than 3A'
c28['3E']='zoom Tele (avoiding digital zoom, some cameras): fastest speed'
c28['41']='Auto-Focus on/off (not if there is a real switch at the camera)'
c28['45']='Focus manual far'
c28['47']='Focus manual near'
c28['49']='White balance toggle (only cameras until approx. 1996)'
c28['4B']='Backlight (not DV)'
c28['51']='Backlight (DV)'
c28['53']='Exposure auto/man. toggle (models of the early 90s)'
c28['54']='Iris more close'
c28['55']='Iris more open'
c28['61']='Shutter (models of the early 90s)'
c28['77']='White balance reset (not if white balance is selected via menu)'
c28['85']='Memory impose (models of the early 90s)'
c28['87']='Color / Mode (models of the early 90s)'
c28['89']='Superimpose (models of the early 90s)'
c28['AF']='Iris auto'

cD8={}
cD8['00']='start/stop'
cD8['01']='mode movie/still'
cD8['02']='photo write'
cD8['03']='power off'
cD8['05']='menu'
cD8['09']='execute'
cD8['0B']='menu right'
cD8['0C']='photo capture'
cD8['0D']='menu left'
cD8['0F']='menu up'
cD8['11']='menu down'
cD8['17']='data screen'

c1E={}
c1E['01']='zoom Tele: slowest speed'
c1E['03']='zoom Tele: faster than 01'
c1E['05']='zoom Tele: faster than 03'
c1E['07']='zoom Tele: faster than 05'
c1E['09']='zoom Tele: faster than 07'
c1E['0B']='zoom Tele: faster than 09'
c1E['0D']='zoom Tele: faster than 0B'
c1E['0F']='zoom Tele: fastest speed'
c1E['11']='zoom Wide: slowest speed'
c1E['13']='zoom Wide: faster than 11'
c1E['15']='zoom Wide: faster than 13'
c1E['17']='zoom Wide: faster than 15'
c1E['19']='zoom Wide: faster than 17'
c1E['1B']='zoom Wide: faster than 19'
c1E['1D']='zoom Wide: faster than 1B'
c1E['1F']='zoom Wide: fastest speed'
c1E['52']='photo preview'
c1E['58']='photo save (or in movie mode: start-stop)'
c1E['5E']='power off'
c1E['94']='Zoom Tele slow'
c1E['96']='Zoom Wide slow'
c1E['98']='Zoom Tele fast'
c1E['9A']='Zoom Wide fast'

# status decoder
b4={}
b4['00']='initial'
b4['01']='is eject'
b4['11']='dew cass. out'
b4['21']='ejecting'
b4['31']='unload'
b4['B1']='unload emerg.'
b4['02']='stop'
b4['12']='load'
b4['22']='cassette busy'
b4['32']='low-battery'
b4['42']='dew stop'
b4['52']='emergency'
b4['62']='tape end'
b4['72']='tape top'
b4['92']='stp after zero'
b4['A2']='load emer.'
b4['B2']='stop emerg. 1'
b4['C2']='stop emerg. 2'
b4['E2']='stop NC'
b4['03']='fwd'
b4['33']='go zero/play f.'
b4['43']='fwd mem stop '
b4['B3']='go zero/play r.'
b4['C3']='rew mem stop'
b4['D3']='hi-speed rew'
b4['04']='rec'
b4['14']='rec/ pause'
b4['24']='timer-rec'
b4['34']='timer-rec s.'
b4['44']='AV insert'
b4['54']='AV ins.-pause'
b4['64']='video insert'
b4['74']='video ins.-ps'
b4['84']='audio dub'
b4['94']='a.dub pause'
b4['A4']='cam rec'
b4['B4']='cam stby'
b4['85']='edit search+'
b4['95']='edit search-'
b4['A5']='edit-s fwd'
b4['B5']='edit-s rev'
b4['F5']='edit pause'
b4['06']='play'
b4['26']='x1 fwd'
b4['36']='x1 rev'
b4['46']='cue'
b4['56']='rev'
b4['66']='x2/x3 fwd'
b4['76']='x2/x3 rev'
b4['86']='x9 fwd'
b4['96']='x9 rev'
b4['A6']='frame sea. cue'
b4['B6']='frame sea. rev'
b4['C6']='x14 fwd'
b4['D6']='x14 rev'
b4['07']='play/pause fwd'
b4['17']='frame fwd'
b4['27']='1/5 fwd'
b4['37']='1/5 rev'
b4['47']='1/10 fwd'
b4['57']='1/10 rev'
b4['67']='frame fwd'
b4['77']='frame rev'
b4['97']='play/pause rev'
b4['08']='AL insert'
b4['18']='AL ins-pause'
b4['28']='AR insert'
b4['38']='AR ins-pause'
b4['48']='AL+V insert'
b4['58']='AL+V ins-ps'
b4['68']='AR+V insert'
b4['78']='AL+R ins-ps'
b4['ED']='mpeg movie mode'
b4['EE']='photo mode'
b4['DF']='play mode'
b4['EF']='setup mode'


   
class Lanc(HighLevelAnalyzer):

    # command type
    command_value = '0'
    # timing of the last received byte
    last_frame_end = None
    # byte number in frame
    byte_no = 9

    # An optional list of types this analyzer produces, providing a way to customize the way frames are displayed in Logic 2.
    result_types = {
        'mytype': {
            'format': '0x{{data.inv}} {{data.binary}}'
        }
    }

    def __init__(self):
        #      self.my_number_setting, self.my_choices_setting)
        print('Init')
                  

    def decode(self, frame: AnalyzerFrame):
    
        # invert the byte, as LANC uses inverted signals   
        inv = bytes(x^0xFF for x in frame.data['data'])
        inv_formatted = inv.hex().upper()
        
        command = ''
        self.byte_no += 1
        # bits 
        binary = '{:08b}'.format(int.from_bytes(inv, byteorder='big'))
            
        if self.command_value == '18':
            command = c18.get(inv_formatted)
            if command is None:
                command = ''
            else:
                command = 'C#18 ' + command
        elif self.command_value == '28':
            command = c28.get(inv_formatted)
            if command is None:
                command = ''
            else:
                command = 'C#28 ' + command
        elif self.command_value == 'D8':
            command = cD8.get(inv_formatted)
            if command is None:
                command = ''
            else:
                command = 'C#D8 ' + command
        elif self.command_value == '1E':
            command = c1E.get(inv_formatted)
            if command is None:
                command = ''
            else:
                command = 'C#1E ' + command
                           
        # frame detection
        if self.last_frame_end:
            delta = frame.start_time - self.last_frame_end
                    
            # more than 7 ms between chars, must be a new LANC frame
            if float(delta) > 0.007:
                self.byte_no = 0
                self.command_value = inv_formatted
            else:
                self.command_value = '0'
                
        self.last_frame_end = frame.end_time
        
        status = ''
        # camera status byte is number 4 (5th byte)
        if self.byte_no == 4:
            status = b4.get(inv_formatted)
            if status is None:
                status = ''
            else:
                status = 'S# ' + status            

        # Return the data frame
        return AnalyzerFrame('mytype', frame.start_time, frame.end_time, {
            'inv': inv_formatted,
            'binary': binary,
            'command': command,
            'status': status,
            'byte_no': str(self.byte_no)
        })
        
    
