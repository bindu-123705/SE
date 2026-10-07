import pygame
import random
import json
import os
from game.player import Player,LANE_W
from game.traffic import Car,MovingLog,make_car

LANES=8
WIDTH=LANES*LANE_W
HEIGHT=600
FPS=60
BG=(60,60,60)
SAFE_LANE_Y=260
SAFE_LANE_H=80
HIGH_SCORE_FILE="high_scores.json"
DAY_NIGHT_INTERVAL=30*FPS

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",24,bold=True)
        self.big_font=pygame.font.SysFont("monospace",44,bold=True)
        self.high_scores=self.load_high_scores()
        self.score_saved=False
        self.reset()

    def load_high_scores(self):
        if not os.path.exists(HIGH_SCORE_FILE):
            return []
        try:
            with open(HIGH_SCORE_FILE,"r") as f:
                scores=json.load(f)
            if not isinstance(scores,list):
                return []
            scores=[int(score) for score in scores]
            return sorted(scores,reverse=True)[:5]
        except (OSError,ValueError,TypeError,json.JSONDecodeError):
            return []

    def save_high_score(self):
        if self.score_saved:
            return
        self.high_scores.append(self.score//10)
        self.high_scores=sorted(self.high_scores,reverse=True)[:5]
        try:
            with open(HIGH_SCORE_FILE,"w") as f:
                json.dump(self.high_scores,f)
        except OSError:
            pass
        self.score_saved=True

    def reset(self):
        self.player=Player(4*LANE_W+LANE_W//2,HEIGHT-80)
        self.cars=[]
        self.log=MovingLog(SAFE_LANE_Y+20,LANE_W*2,2.5,WIDTH)
        self.riding_log=False
        self.timer=0
        self.spawn_interval=50
        self.speed=3
        self.score=0
        self.lives=3
        self.day_night_timer=0
        self.is_night=False
        self.game_over=False
        self.won=False
        self.score_saved=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_r:
                self.reset()
        return True

    def update(self):
        if self.game_over or self.won: return
        self.day_night_timer+=1
        if self.day_night_timer>=DAY_NIGHT_INTERVAL:
            self.day_night_timer=0
            self.is_night=not self.is_night
        keys=pygame.key.get_pressed()
        old_y=self.player.rect.y
        self.player.move(keys,0,WIDTH)

        self.timer+=1
        if self.timer>=self.spawn_interval:
            lane=random.randint(0,LANES-1)
            self.cars.append(make_car(lane,HEIGHT,self.speed))
            self.timer=0
            self.spawn_interval=max(22,self.spawn_interval-0.2)

        self.log.update()
        if self.riding_log:
            self.player.rect.x+=self.log.dx
            self.player.rect.x=max(0,min(WIDTH-self.player.rect.width,self.player.rect.x))
        
        if self.riding_log:
            self.player.rect.left=max(self.player.rect.left,self.log.rect.left)
            self.player.rect.right=min(self.player.rect.right,self.log.rect.right)

        in_log_lane=(self.player.rect.centery>=SAFE_LANE_Y and self.player.rect.centery<=SAFE_LANE_Y+SAFE_LANE_H)
        on_log=self.player.rect.colliderect(self.log.rect)
        if in_log_lane and not on_log and not self.riding_log:
            self.player.rect.y=old_y
            in_log_lane=False
        elif self.riding_log and not on_log:
            self.riding_log=False

            if not in_log_lane:
                lane_idx=round(self.player.rect.centerx/LANE_W-0.5)
                lane_idx=max(0,min(LANES-1,lane_idx))
                self.player.rect.centerx=lane_idx*LANE_W+LANE_W//2

        if in_log_lane and on_log:
            self.riding_log=True

        for c in self.cars:
            c.update()
            if c.rect.colliderect(self.player.rect) and not self.riding_log:
                self.lives-=1
                self.cars.remove(c)
                if self.lives<=0:
                    self.game_over=True
                break
        self.cars=[c for c in self.cars if not c.off_screen(HEIGHT)]

        self.score+=1
        if self.score%300==0: self.speed=min(10,self.speed+0.5)
        if self.player.rect.top<=10:
            self.won=True
            self.save_high_score()

    def draw(self):
        if self.is_night:
            self.screen.fill((10,15,30))
        else:
            self.screen.fill(BG)
        # road markings
        for i in range(LANES+1):
            road_line_color=(55,55,70) if self.is_night else (100,100,100)
            pygame.draw.line(self.screen,road_line_color,(i*LANE_W,0),(i*LANE_W,HEIGHT),2)
        for y in range(0,HEIGHT,60):
            for i in range(LANES):
                marking_color=(150,150,80) if self.is_night else (200,200,100)
                pygame.draw.rect(self.screen,marking_color,pygame.Rect(i*LANE_W+LANE_W//2-3,y,6,30))
        # moving log lane
        pygame.draw.rect(self.screen,(40,90,130),pygame.Rect(0,SAFE_LANE_Y,WIDTH,SAFE_LANE_H))
        self.log.draw(self.screen)

        # sidewalks
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,HEIGHT-50,WIDTH,50))
        pygame.draw.rect(self.screen,(150,130,110),pygame.Rect(0,0,WIDTH,30))
        for c in self.cars: c.draw(self.screen,self.is_night)
        self.player.draw(self.screen)
        hud=pygame.Rect(0,0,WIDTH,30)
        pygame.draw.rect(self.screen,(20,20,20),hud)
        period="NIGHT" if self.is_night else "DAY"
        s=self.font.render(f"Score: {self.score//10}  Lives: {self.lives}  {period}  GOAL: reach the top!  R=Restart",True,(220,220,220))
        self.screen.blit(s,(6,4))
        if self.game_over:
            self._msg("CRASHED!",(220,60,60))
        if self.won:
            self._msg("YOU MADE IT!",(80,220,80))
        self._draw_high_scores()
        pygame.display.flip()

    def _draw_high_scores(self):
        title=self.font.render("TOP 5",True,(220,220,220))
        self.screen.blit(title,(WIDTH-100,40))
        for i,score in enumerate(self.high_scores):
            text=self.font.render(f"{i+1}. {score}",True,(220,220,220))
            self.screen.blit(text,(WIDTH-100,70+i*28))

    def _msg(self,text,color):
        ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,150))
        self.screen.blit(ov,(0,0))
        m=self.big_font.render(text,True,color)
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,HEIGHT//2+20))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()