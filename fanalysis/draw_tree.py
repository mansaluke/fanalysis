
class draw_tree():
    
    def __init__(self, xe, r, len):
        self.xe, self.r, self.len = xe, r, len
        self.xlim = [0, self.xe + 1]
        self.ylim = [-r-len, r+len]
        
        fig, self.ax = plt.subplots(frameon=False)
    
        #xlim = [0, 6]
        #ylim = [-5, 5]
        
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_aspect(1.)
        
        self.out_tree(self.xe, self.r, self.len)  
    
    
    def out_tree(self, xe=3, r = 0.25, len = 0.75):
        """
        xe = num of nodes, r= radius, len = length of lines
        """    
        
        b=[0]
        self.ax.add_patch(Circle((r, 0), r, facecolor='none', edgecolor = 'black')) 
        
        self.ax.add_line(lines.Line2D([r, r], [r, len], color = 'black'))
        self.ax.add_line(lines.Line2D([r, len], [len, len], color = 'black'))
        self.ax.add_line(lines.Line2D([r, r], [-r, -len], color = 'black'))
        self.ax.add_line(lines.Line2D([r, len], [-len, -len], color = 'black'))
        
        for x in range(1, xe):
            a = b
            b=[]
            
            for i in tuple(a):      
                
                b.append(i+1)
                b.append(i-1)
                
            for i in tuple(b):  
                
                self.ax.add_patch(Circle((r+(x*len), i*len), r, facecolor='none', edgecolor = 'black'))            
    
                self.ax.add_line(lines.Line2D([r+(x*len), r+(x*len)], [r+(i*len), len+(i*len)], color = 'black'))
                self.ax.add_line(lines.Line2D([r+(x*len), len+(x*len)], [len+(i*len), len+(i*len)], color = 'black'))
                
                self.ax.add_line(lines.Line2D([r+(x*len), r+(x*len)], [-r+(i*len), -len+(i*len)], color = 'black'))
                self.ax.add_line(lines.Line2D([r+(x*len), len+(x*len)], [-len+(i*len), -len+(i*len)], color = 'black'))
        
    
        for x in range(xe, xe+1):
            a = b
            b=[]
            
            for i in tuple(a): 
                
                b.append(i+1)
                b.append(i-1)
            for i in tuple(b):
                    
                self.ax.add_patch(Circle((r+(x*len), i*len), r, facecolor='none', edgecolor = 'black'))   
            
                      

draw_tree(5, 0.25, 0.75)