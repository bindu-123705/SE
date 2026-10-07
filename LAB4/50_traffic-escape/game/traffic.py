import pygame
import random

LANE_W=80
COLORS=[(220,60,60),(220,140,40),(140,60,180),(60,180,80),(180,180,40),(60,80,200)]

class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect=pygame.Rect(lane_x+10,y,60,80)
        self.direction=direction  # 1=down, -1=up
        self.speed=speed
        self.color=random.choice(COLORS)

    def update(self):
        self.rect.y+=self.direction*self.speed

    def off_screen(self,height):
        return self.rect.top>height+100 or self.rect.bottom<-100

    def draw(self,screen,night=False):
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        if night:
            beam_surface=pygame.Surface((screen.get_width(),screen.get_height()),pygame.SRCALPHA)
            if self.direction==1:
                beam=[
                    (self.rect.centerx-14,self.rect.bottom),
                    (self.rect.centerx+14,self.rect.bottom),
                    (self.rect.centerx+70,self.rect.bottom+180),
                    (self.rect.centerx-70,self.rect.bottom+180)
                ]
                headlight_y=self.rect.bottom-18
            else:
                beam=[
                    (self.rect.centerx-14,self.rect.top),
                    (self.rect.centerx+14,self.rect.top),
                    (self.rect.centerx+70,self.rect.top-180),
                    (self.rect.centerx-70,self.rect.top-180)
                ]
                headlight_y=self.rect.top+8
            pygame.draw.polygon(beam_surface,(255,245,180,45),beam)
            screen.blit(beam_surface,(0,0))
            pygame.draw.rect(screen,(255,245,180),pygame.Rect(self.rect.x+10,headlight_y,12,8),border_radius=3)
            pygame.draw.rect(screen,(255,245,180),pygame.Rect(self.rect.right-22,headlight_y,12,8),border_radius=3)
        pygame.draw.rect(screen,(180,220,240),pygame.Rect(self.rect.x+8,self.rect.y+10,44,22),border_radius=4)
        for wx in [self.rect.x+6,self.rect.right-16]:
            for wy in [self.rect.y+4,self.rect.bottom-16]:
                pygame.draw.rect(screen,(30,30,30),pygame.Rect(wx,wy,10,12),border_radius=3)

class MovingLog:
    def __init__(self, y, width, speed, screen_width):
        self.rect=pygame.Rect(0,y,width,40)
        self.speed=speed
        self.direction=1
        self.screen_width=screen_width
        self.dx=0

    def update(self):
        self.dx=self.speed*self.direction
        self.rect.x+=self.dx
        if self.rect.left<=0:
            self.rect.left=0
            self.direction=1
        elif self.rect.right>=self.screen_width:
            self.rect.right=self.screen_width
            self.direction=-1

    def draw(self,screen):
        pygame.draw.rect(screen,(120,75,35),self.rect,border_radius=12)
        pygame.draw.rect(screen,(170,110,55),pygame.Rect(self.rect.x+8,self.rect.y+7,self.rect.width-16,8),border_radius=4)

def make_car(lane_idx,height,speed):
    x=lane_idx*LANE_W
    direction=1 if lane_idx%2==0 else -1
    y=-90 if direction==1 else height+10
    return Car(x,y,direction,speed)