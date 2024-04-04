
import idlelib.colorizer as c
import idlelib.percolator as p

class TemaManager:
    def __init__(self, area_texto):
        self.cdg = c.ColorDelegator()
        self.per = p.Percolator(area_texto.text_area)
        #color_fondo=area_texto.text_area.cget('')
        self.per.insertfilter(self.cdg)


    def tema_1(self,back):
        self.aplicar_tema('#2c8100', '#4030FD', '#FEF788', '#FCB54E', '#FEF788',back)

    def tema_2(self,back):
        self.aplicar_tema('#B4B4B4', '#69DDFF', '#B1E5D1', '#FCF66C', '#CEC85A',back)

    def tema_3(self,back):
        self.aplicar_tema('#ECE2C6', '#7FB5B5', '#E4007C', '#FFC3F1', '#D7AECC',back)
        
    def predeterminado(self,back):
        self.aplicar_tema('#FF0000', '#007F00', '#7F7F00', '#7F3F00', '#007F7F',back)
        
    def aplicar_tema(self, comment, keyword, builtin, string, definition,back):
        self.cdg.tagdefs['COMMENT'] = {'foreground': comment, 'background': back}
        self.cdg.tagdefs['KEYWORD'] = {'foreground': keyword, 'background': back}
        self.cdg.tagdefs['BUILTIN'] = {'foreground': builtin, 'background': back}
        self.cdg.tagdefs['STRING'] = {'foreground': string, 'background': back}
        self.cdg.tagdefs['DEFINITION'] = {'foreground': definition, 'background': back}
        self.cdg.config_colors()





    


import idlelib.colorizer as c
import idlelib.percolator as p

class TemaManager:
    def __init__(self, area_texto):
        self.cdg = c.ColorDelegator()
        self.per = p.Percolator(area_texto.text_area)
        #color_fondo=area_texto.text_area.cget('')
        self.per.insertfilter(self.cdg)


    def tema_1(self,back):
        self.aplicar_tema('#2c8100', '#4030FD', '#FEF788', '#FCB54E', '#FEF788',back)

    def tema_2(self,back):
        self.aplicar_tema('#B4B4B4', '#69DDFF', '#B1E5D1', '#FCF66C', '#CEC85A',back)

    def tema_3(self,back):
        self.aplicar_tema('#ECE2C6', '#7FB5B5', '#E4007C', '#FFC3F1', '#D7AECC',back)
        
    def predeterminado(self,back):
        self.aplicar_tema('#FF0000', '#007F00', '#7F7F00', '#7F3F00', '#007F7F',back)
        
    def aplicar_tema(self, comment, keyword, builtin, string, definition,back):
        self.cdg.tagdefs['COMMENT'] = {'foreground': comment, 'background': back}
        self.cdg.tagdefs['KEYWORD'] = {'foreground': keyword, 'background': back}
        self.cdg.tagdefs['BUILTIN'] = {'foreground': builtin, 'background': back}
        self.cdg.tagdefs['STRING'] = {'foreground': string, 'background': back}
        self.cdg.tagdefs['DEFINITION'] = {'foreground': definition, 'background': back}
        self.cdg.config_colors()





    
