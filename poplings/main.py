import pygame
import random
import sys
import popling
import food

#zooming is not possible(main aspect)
#problems:
#problem 1: fix the seeking problem

#Ideas
#when popling eat food they grow
#when popling reach maximum health it is given chance to increase size but reducing current health to half
#introduce option to view generations and veg and non-veg




pygame.init()


window = pygame.display.set_mode((500,500), pygame.RESIZABLE)
pygame.display.set_caption('poplings')
fps = pygame.time.Clock()


poplings = []
for i in range(1, 26):
    p = popling.Popling()
    poplings.append(p)

f1 = food.Food([500,500])
f2 = food.Food([500,500])
foodBlock = [f1, f2]

f_count = 250

veg_count = 25
non_veg_count = 0

births = 0
deaths = 0

seekingPop = None


while True:
    #checking events
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

    window.fill(pygame.Color(255,255,255))
    
    f_count -= 1
    if f_count==0:
        f = food.Food([int(window.get_width()), int(window.get_height())])
        foodBlock.append(f)
        f_count = 250
    

    if len(poplings)<10:
        p = popling.Popling()
        veg_count += 1
        poplings.append(p)
   
    #diplyaing poplings
    mouse_x, mouse_y = pygame.mouse.get_pos()
    onClick = False
    for pop in poplings:
        pop.bounds = [int(window.get_width()), int(window.get_height())]
        pop.move(foodBlock, poplings)
        ranp = random.random()
        if ranp <0.0001:
            p = pop.reproduce()
            births += 1
            if p.dna.eatingHabit == "Veg":
                veg_count +=1
            else:
                non_veg_count +=1
            poplings.append(p)
        pop.health -= 0.1
        if pop.health<0:
            pop.die(foodBlock)
            deaths += 1
            if pop.dna.eatingHabit == "Veg":
                veg_count -= 1
            else:
                non_veg_count -= 1
            poplings.remove(pop)
            continue
        pygame.draw.circle(window, pop.dna.color, (pop.x, pop.y), pop.radius, 1)
        
        if pop.dist( mouse_x, mouse_y) < pop.radius:
            STAT_FONT = pygame.font.SysFont("comicsansms", pop.radius//2)
            text = STAT_FONT.render(str(int(pop.health)), 1, (255,0,0))
            window.blit(text, (pop.x - pop.radius//2, pop.y - pop.radius//2))
            if click:
                seekingPop = pop
                onClick = True

    #displaying food
    for f in foodBlock:
        if f.type == "Non-Veg":
            pygame.draw.circle(window, pygame.Color(255, 0, 0), (f.x, f.y), f.radius, 1)
        else:
            pygame.draw.circle(window, (0,255,0), (f.x, f.y), f.radius, 1)
    
    if not onClick and click:
        seekingPop = None
    
    #displaying information about the selected one
    if seekingPop != None:
        if seekingPop in poplings:
            base = pygame.Surface((160, 160))
            base.fill((235,235,235))
            window.blit(base, (10,10))
            STAT_FONT2 = pygame.font.SysFont("comicsansms", 20)
            health_info = STAT_FONT2.render("Max health= " + str(int(seekingPop.maxHealth)), 1, (0,0,0))
            current_health_info = STAT_FONT2.render("Health= "+ str(int(seekingPop.health)), 1, (0,0,0))
            speed_info = STAT_FONT2.render("Speed= " + str(int(seekingPop.velocity)), 1, (0,0,0))
            generation_info = STAT_FONT2.render("GEN=" + str(seekingPop.generation), 1, (0,0,0))
            eating_info = STAT_FONT2.render("eatingHabit= " + seekingPop.dna.eatingHabit, 1, (0,0,0))
            window.blit(generation_info, (12,15))
            window.blit(health_info, (12, 40))
            window.blit(current_health_info, (12, 65))
            window.blit(speed_info, (12, 90))
            window.blit(eating_info, (12, 115))
        else:
            seekingPop = None
    STAT_FONT = pygame.font.SysFont("comicsansms", 20)
    t = "births: " + str(births) + "  deaths: " + str(deaths)
    t2 = "Veg: " + str(veg_count)
    t3 = "Non-Veg: " + str(non_veg_count)
    population_info = STAT_FONT.render(t, 1, (0,0,0))
    veg_info = STAT_FONT.render(t2, 1, (0,255,0))
    non_veg_info = STAT_FONT.render(t3, 1, (255, 0, 0))
    window.blit(population_info, (window.get_width()- len(t)*10 - 10, 15))
    window.blit(veg_info, (window.get_width() - 210, 50))
    window.blit(non_veg_info, (window.get_width() - 210, 85))

    #base condition
    if len(poplings) == 0:
        pygame.quit()
        sys.exit()

    
    pygame.display.flip()
    fps.tick(200)


        