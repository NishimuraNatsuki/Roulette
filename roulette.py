import tkinter as tk
import random
import math

class RouletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ルーレット")
        
        #フレームを設定
        self.ui_frame = tk.Frame(self.root)
        self.ui_frame.grid(row=0,column=0)
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row=1,column=0)
        self.roulette_frame = tk.Frame(self.root)      
        self.roulette_frame.grid(row=1,column=1)
        
        #エントリーボックス
        self.entries = [tk.Entry(self.entry_frame)]
        
        #針の回転
        self.flag = False
        self.rug_count = 0
        
        #画面サイズ
        self.width = 400
        self.height = 500
        self.centerx = self.width/2
        self.centery = self.height * 0.4
        self.length = self.width * 0.4
        
        self.result = ''
        
        self.make_ui()
        self.roulette(1)
        
    def make_ui(self):
        #エントリーの追加、削除
        def add_entry(event):
            self.entries.append(tk.Entry(self.entry_frame))
            self.entries[-1].pack()

        def del_entry(event):
            if(self.entries != []):
                self.entries[-1].destroy()
                del self.entries[-1]
            else:
                pass
            
        self.canvas = tk.Canvas(self.roulette_frame, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        
        self.entries[-1].pack()
        
        
        #ボタン
        plus_button = tk.Button(self.ui_frame, text='項目を追加')
        plus_button.bind("<Button-1>",add_entry)
        plus_button.pack(side=tk.LEFT)

        minus_button = tk.Button(self.ui_frame,text='項目を削除')
        minus_button.bind("<Button-1>",del_entry)
        minus_button.pack(side=tk.LEFT)
        
        gene_button = tk.Button(self.ui_frame,text='適用')
        gene_button.bind("<Button-1>",self.roulette)
        gene_button.pack(side=tk.LEFT)
                
        self.spin_button = tk.Button(self.roulette_frame,text='回す')
        self.spin_button.bind("<Button-1>",self.flagjudge)
        self.spin_button.pack()
        
        
    def roulette(self,event):        
        self.canvas.delete("all")
        
        self.texts = []
        #エントリーから要素抽出
        for entry in self.entries:
            self.texts.append(entry.get())
                    
        tkinter_color_list = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta','purple','black','gray']
        
        colors = random.choices(tkinter_color_list,k=len(self.entries))
        
        if(len(self.entries) != 0):
            #0.0001は描画のために微調整  
            self.angle = 0
            self.segments = len(self.entries)          
            self.segments_angle = 360 / self.segments -0.0001
            x0, y0, x1, y1 = self.centerx-self.length, self.centery-self.length, self.centerx+self.length, self.centery+self.length
            
            for i in range(self.segments):
                start_angle = i * self.segments_angle +0.0001 % 360
                self.canvas.create_arc(x0, y0, x1, y1, start=start_angle, extent=self.segments_angle,width=3,outline=colors[i])
                self.canvas.create_text(self.centerx+self.length/2*math.cos(math.radians(start_angle+(self.segments_angle/2))), self.centery+self.length/2*math.sin(math.radians(start_angle+(self.segments_angle/2))), text = self.texts[i],font=('normal',25))
                self.needle = self.canvas.create_line(self.centerx, self.centery, self.centerx+self.length* math.cos(math.radians(self.angle)), self.centery + self.length * math.sin(math.radians(self.angle)), width=3, fill="black")
            
        else:
            pass
        
        self.canvas.update()
        
    def flagjudge(self,event):   
        if(self.flag):
            self.spin_button['text'] = '回す'
            self.flag = False
            self.rug_spin()
            
        else:
            self.spin_button['text'] = '止める'
            self.flag = True
            self.rug_count = 0
            self.canvas.delete(self.result)
            self.spin()
    
    def spin(self):
        if(self.angle >= 360):
            self.angle = 0

        self.canvas.delete(self.needle)
        if(self.flag):
            self.angle += 10
            self.needle = self.canvas.create_line(self.centerx, self.centery, self.centerx+self.length* math.cos(math.radians(self.angle)), self.centery+ self.length * math.sin(math.radians(self.angle)), width=3, fill="black")
            self.root.after(50, self.spin)

    def rug_spin(self):
        if(self.angle >= 360):
            self.angle = 0
        #rugは100で設定
        if(self.rug_count < 100):
            self.canvas.delete(self.needle)
            self.angle += 10/(0.1 * self.rug_count + 1) 
            self.needle = self.canvas.create_line(self.centerx, self.centery, self.centerx+self.length* math.cos(math.radians(self.angle)), self.centery+ self.length * math.sin(math.radians(self.angle)), width=3, fill="black")
            self.rug_count += 1
            if(self.rug_count < 100):
                self.root.after(50, self.rug_spin)
            else:
                #針が止まった時
                self.result = self.canvas.create_text(self.centerx, self.height - self.length/2, text = self.texts[int(self.angle/self.segments_angle)],font=('normal',25),fill = 'red')
                        
    

if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteApp(root)
    # app.setup()
    root.mainloop()