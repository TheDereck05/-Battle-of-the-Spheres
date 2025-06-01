from tkinter.filedialog import askopenfilename
import pygame
import sys
import math
import random
from tkinter import Tk
from tkinter.colorchooser import askcolor
import os
import colorsys

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)

# Inicializa el mixer de sonido
pygame.init()

# 1) Carpeta donde está este archivo Esfera.py
BASE_DIR = os.path.dirname(__file__)  
# 2) Carpeta de assets/imagenes dentro de game/
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "imagenes")
# 3) Carpeta de sonidos dentro de assets
sonido_path = os.path.join(BASE_DIR, "assets", "sonidos")

sonido_rebote = pygame.mixer.Sound(os.path.join(sonido_path, "rebote.wav"))
sonido_vida   = pygame.mixer.Sound(os.path.join(sonido_path, "vida_song.wav"))
sonido_katana = pygame.mixer.Sound(os.path.join(sonido_path, "katana.wav"))
sonido_pegar  = pygame.mixer.Sound(os.path.join(sonido_path, "pegar.wav"))

# Ajustar volúmenes (ejemplos)
sonido_rebote.set_volume(0.1)   #
sonido_vida.set_volume(0.1)     
sonido_katana.set_volume(0.3)   
sonido_pegar.set_volume(0.2)

def elegir_color():
    root = Tk()
    root.withdraw()
    c = askcolor()[0]
    return c if c else (255, 255, 255)

def seleccionar_imagen():
    root = Tk()
    root.withdraw()
    filename = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return filename if filename else None

def menu_configuracion():
    pygame.init()
    ANCHO, ALTO = 480, 850
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Configurar Jugadores")

    NEGRO = (10, 10, 10)
    BLANCO = (240, 240, 240)
    AZUL_CLARO = (100, 200, 255)
    FUENTE = pygame.font.SysFont(None, 36)
    TITULO = pygame.font.SysFont(None, 52)

    nombre1 = ""
    nombre2 = ""
    activo = 0
    color1 = (255, 0, 0)
    color2 = (0, 0, 255)
    img1_path = ""
    img2_path = ""
    tiempo_min = ""

    input1_rect = pygame.Rect(90, 230, 300, 50)
    input2_rect = pygame.Rect(90, 350, 300, 50)
    color1_rect  = pygame.Rect(90, 470, 300, 50)
    color2_rect  = pygame.Rect(90, 530, 300, 50)
    img1_rect    = pygame.Rect(90, 620, 300, 50)
    img2_rect    = pygame.Rect(90, 680, 300, 50)
    tiempo_rect = pygame.Rect(90, 750, 300, 50)

    cursor_visible = True
    cursor_timer = 0
    reloj = pygame.time.Clock()

    def render_input(texto, rect, activo_bool):
        nonlocal cursor_visible
        borde = AZUL_CLARO if activo_bool else BLANCO
        pygame.draw.rect(pantalla, borde, rect, border_radius=8, width=2)
        txt = FUENTE.render(texto, True, BLANCO)
        pantalla.blit(txt, (rect.x+10, rect.y+12))
        if activo_bool and cursor_visible:
            x = rect.x+10+txt.get_width()+2
            pygame.draw.line(pantalla, BLANCO, (x, rect.y+10), (x, rect.y+40), 2)

    def dibujar():
        pantalla.fill(NEGRO)
        t = TITULO.render("Configurar Jugadores", True, BLANCO)
        pantalla.blit(t, ((ANCHO - t.get_width()) // 2, 100))

        render_input(nombre1 or "Jugador 1", input1_rect, activo == 1)
        render_input(nombre2 or "Jugador 2", input2_rect, activo == 2)

        pygame.draw.rect(pantalla, color1, color1_rect, border_radius=8)
        bt1 = FUENTE.render("Elegir color J1", True, BLANCO)
        pantalla.blit(bt1, (color1_rect.x + 10, color1_rect.y + 12))

        pygame.draw.rect(pantalla, color2, color2_rect, border_radius=8)
        bt2 = FUENTE.render("Elegir color J2", True, BLANCO)
        pantalla.blit(bt2, (color2_rect.x + 10, color2_rect.y + 12))

        pygame.draw.rect(pantalla, AZUL_CLARO, img1_rect, border_radius=8)
        im1 = FUENTE.render("Elegir imagen J1", True, NEGRO)
        pantalla.blit(im1, (img1_rect.x + 10, img1_rect.y + 12))

        pygame.draw.rect(pantalla, AZUL_CLARO, img2_rect, border_radius=8)
        im2 = FUENTE.render("Elegir imagen J2", True, NEGRO)
        pantalla.blit(im2, (img2_rect.x + 10, img2_rect.y + 12))

        render_input(tiempo_min or "Duración (min)", tiempo_rect, activo == 3)

        inst = FUENTE.render("ENTER para continuar", True, BLANCO)
        pantalla.blit(inst, ((ANCHO - inst.get_width()) // 2, img2_rect.bottom + 80))

        pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if e.type == pygame.MOUSEBUTTONDOWN:
                if input1_rect.collidepoint(e.pos):
                    activo = 1
                elif input2_rect.collidepoint(e.pos):
                    activo = 2
                elif tiempo_rect.collidepoint(e.pos):
                    activo = 3
                elif color1_rect.collidepoint(e.pos):
                    color1 = elegir_color()
                elif color2_rect.collidepoint(e.pos):
                    color2 = elegir_color()
                elif img1_rect.collidepoint(e.pos):
                    img1_path = seleccionar_imagen()
                elif img2_rect.collidepoint(e.pos):
                    img2_path = seleccionar_imagen()
                else:
                    activo = 0

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and nombre1.strip() and nombre2.strip() and tiempo_min.strip():
                    pygame.quit()
                    return nombre1, nombre2, color1, color2, img1_path, img2_path, tiempo_min
                
                if e.key == pygame.K_BACKSPACE:
                    if activo==1: 
                        nombre1 = nombre1[:-1]
                    elif activo==2: 
                        nombre2 = nombre2[:-1]
                    elif activo ==3:
                        tiempo_min = tiempo_min[:-1]

                elif e.unicode.isprintable():
                    if activo==1 and len(nombre1)<100000: nombre1 += e.unicode
                    if activo==2 and len(nombre2)<100000: nombre2 += e.unicode
                    elif activo==3 and len(tiempo_min) <3 and e.unicode.isdigit(): #si el if no es correcto cambialo por elif 
                        tiempo_min += e.unicode 

        cursor_timer += reloj.get_time()
        if cursor_timer >= 500:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        dibujar()
        reloj.tick(60)

def crear_superficie_con_borde(imagen, radio):
    diametro = radio * 2  # Calculamos el diámetro basado en el radio

    # Redimensionar la imagen al tamaño adecuado
    imagen = pygame.transform.smoothscale(imagen, (diametro, diametro))

    # Crear una máscara circular para recortar la imagen
    mask = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)

    # Establecer el color transparente y aplicar la máscara
    imagen.set_colorkey((0, 0, 0))  # Esto asegura que los píxeles transparentes se quiten.
    imagen.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    return imagen
class Particle:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.radius = random.randint(3, 6)
        # Color aleatorio para el efecto multicolor
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.lifetime = random.randint(20, 40)  # Duración en frames

    def update(self):
        self.pos += self.vel
        self.lifetime -= 1

    def draw(self, pantalla):
        if self.lifetime > 0:
            pygame.draw.circle(pantalla, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

def explosion(pantalla, clock, centro, cantidad=50):
    particulas = [Particle(centro) for _ in range(cantidad)]
    # Capturamos el estado actual de la pantalla para preservar el fondo
    fondo_actual = pantalla.copy()
    
    while particulas:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # En lugar de limpiar la pantalla con fill, reutilizamos el fondo capturado
        pantalla.blit(fondo_actual, (0, 0))
        
        for p in particulas:
            p.update()
            p.draw(pantalla)
        
        particulas = [p for p in particulas if p.lifetime > 0]
        pygame.display.flip()
        clock.tick(60)
        
def iniciar_juego(nombre1, nombre2, color1, color2, img1_path, img2_path, tiempo_min):
    
    try:
        duracion_min = int(tiempo_min)
        if duracion_min <= 0:
            duracion_min = 2          # si el usuario puso “0” o negativo, asigna 2 min por defecto
    except ValueError:
        duracion_min = 2             # si no ingresó un número, asigna 2 min
    duracion_reloj_ms = duracion_min * 60 * 1000


    inicio_reloj = pygame.time.get_ticks()        # instante (ms) en que arranca la partida
    fin_reloj    = inicio_reloj + duracion_reloj_ms
    juego_terminado_por_tiempo = False            # flag que bloquea la lógica cuando el tiempo llega a cero

    hue = 0.0
    hue_speed = 0.001

    # Hue y velocidad de ciclo para halos de velocidad (más rápido)
    sphere_hue = 0.0
    sphere_hue_speed = 0.02  # mucho más alto → ciclo más rápido

    pygame.init()
    ANCHO, ALTO = 480, 800
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Batalla de Esferas")
    halo_damage_img = pygame.image.load(os.path.join(IMAGE_DIR, "sierra_1-remove.png")).convert_alpha()
    NEGRO = (20, 20, 20)
    battle_rect = pygame.Rect(50, 200, 380, 380)

    class Sphere:
        def __init__(self, r, color, img_path):
            self.r_original = r
            self.r = r
            self.color = color
            self.original_color = color
            self.pos = pygame.Vector2(
                random.uniform(battle_rect.left+r, battle_rect.right-r),
                random.uniform(battle_rect.top+r, battle_rect.bottom-r)
            )
            angle = random.uniform(0, 2*math.pi)
            self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * random.uniform(3,4)

            self.vel_original= self.vel.copy()
            self.vel_timer= None

            self.salud = 5
            self.imagen = pygame.image.load(img_path).convert_alpha() if img_path else None
            self.grafico = crear_superficie_con_borde(self.imagen, r) if self.imagen else None
            self.grafico = crear_superficie_con_borde(self.imagen, r) if self.imagen else None
            self.has_attacked = False
            self.halo_color = color
            self.halo_padding = 5  # O el valor que desees para el halo
            self.is_affected_by_orb = False
            self.halo_damage_img = halo_damage_img
            self.is_affected_by_orb = False

        def move(self): self.pos += self.vel

        def bounce_walls(self):
            rebote = False
            if self.pos.x - self.r < battle_rect.left:
                self.pos.x = battle_rect.left + self.r
                self.vel.x *= -1
                rebote = True
            elif self.pos.x + self.r > battle_rect.right:
                self.pos.x = battle_rect.right - self.r
                self.vel.x *= -1
                rebote = True

            if self.pos.y - self.r < battle_rect.top:
                self.pos.y = battle_rect.top + self.r
                self.vel.y *= -1
                rebote = True
            elif self.pos.y + self.r > battle_rect.bottom:
                self.pos.y = battle_rect.bottom - self.r
                self.vel.y *= -1
                rebote = True

            if rebote:
                sonido_rebote.play()
        def grab_orb_damage(self, orb):
            if self.pos.distance_to(orb.pos) < self.r + orb.r:
                self.is_affected_by_orb = True
                # no cambiamos self.color
                self.is_affected_by_orb = True

        def restore_color(self):
            self.is_affected_by_orb = False
            # no tocamos self.color
            self.halo_color = self.original_color

        def draw(self):
            draw_pos = (int(self.pos.x), int(self.pos.y))
            halo_radius = int(self.r + self.halo_padding)

            if self.is_affected_by_orb:
                # Escalamos la imagen para que tenga el mismo tamaño que el halo circular
                img = pygame.transform.smoothscale(
                    self.halo_damage_img,
                    (halo_radius * 2, halo_radius * 2)
                )
                rect = img.get_rect(center=draw_pos)
                pantalla.blit(img, rect)
            else:
                pygame.draw.circle(pantalla, self.halo_color, draw_pos, halo_radius)

            # esfera interior:
            if self.grafico:
                inner_rect = self.grafico.get_rect(center=draw_pos)
                pantalla.blit(self.grafico, inner_rect)
            else:
                pygame.draw.circle(pantalla, self.color, draw_pos, self.r)

        def change_health(self, a):
            # Cambiar la salud y asegurar que esté entre 0 y 5
            self.salud = max(0, min(self.salud + a, 5))

            # Si la salud está entre 1 y 5, el tamaño se ajusta proporcionalmente
            if self.salud == 5:  # Si está al máximo de vida
                self.r = self.r_original  # Tamaño original
            elif self.salud == 4:  # Primer paso de reducción
                self.r = self.r_original - (self.r_original - 30) * 1/4
            elif self.salud == 3:  # Segundo paso de reducción
                self.r = self.r_original - (self.r_original - 30) * 2/4
            elif self.salud == 2:  # Tercer paso de reducción
                self.r = self.r_original - (self.r_original - 30) * 3/4
            elif self.salud == 1:  # Último paso de reducción (tamaño mínimo)
                self.r = 30  # Límite mínimo de tamaño

            # Si tiene imagen, regenerar la superficie con el nuevo tamaño
            if self.imagen:
                self.grafico = crear_superficie_con_borde(self.imagen, self.r)
        def reset_velocidad(self):   
            self.vel = self.vel_original.copy()
            self.vel_timer = None
            self.halo_color = self.original_color
            global tiempo_velocidad
            tiempo_velocidad = pygame.time.get_ticks()



    def collide(a, b):
            # Radios efectivos (esfera principal + padding del halo)
        ra = a.r + a.halo_padding
        rb = b.r + b.halo_padding
        delta = b.pos - a.pos

        dist = delta.length()
        if dist == 0 or dist >= ra + rb:

            return
        
        sonido_rebote.play()

        # Separación suave
        overlap = (ra+rb) - dist
        d = delta.normalize()
        a.pos -= d * (overlap / 2)
        b.pos += d * (overlap / 2)

        # Rebote físico
        n = d
        t = pygame.Vector2(-n.y, n.x)
        v1n = n.dot(a.vel); v1t = t.dot(a.vel)
        v2n = n.dot(b.vel); v2t = t.dot(b.vel)
        a.vel = n * v2n + t * v1t
        b.vel = n * v1n + t * v2t
        a.vel = a.vel.normalize() * a.vel.length()
        b.vel = b.vel.normalize() * b.vel.length()

        # DAÑO desde a hacia b
        if a.is_affected_by_orb and not a.has_attacked:
            b.change_health(-1)
            sonido_pegar.play()
            a.has_attacked = True
            a.is_affected_by_orb = False   # se quita el halo-daño de a

        # DAÑO desde b hacia a
        if b.is_affected_by_orb and not b.has_attacked:
            a.change_health(-1)
            sonido_pegar.play()
            b.has_attacked = True
            b.is_affected_by_orb = False   # se quita el halo-daño de b



    class Orb:
        def __init__(self, c, t):
            # c: color de respaldo si no carga imagen
            # t: 'vida' o 'ataque'
            self.color = c
            self.tipo  = t
            self.r     = 10
            self.pos   = pygame.Vector2(
                random.uniform(battle_rect.left  + self.r, battle_rect.right  - self.r),
                random.uniform(battle_rect.top   + self.r, battle_rect.bottom - self.r)
            )

            # Seleccionar archivo según tipo
            if t == "vida":
                nombre = "vida.png"
            elif t == "ataque":
                nombre = "danio.png"
            elif t == "velocidad":
                nombre = "velocidad.png"
            else:
                raise ValueError(f"Tipo de orbe desconocido: {t}")
            ruta   = os.path.join(IMAGE_DIR, nombre)

            # Cargar y escalar imagen
            try:
                img = pygame.image.load(ruta).convert_alpha()
                self.imagen = pygame.transform.smoothscale(img, (2*self.r, 2*self.r))
            except Exception as e:
                print(f"No pude cargar {ruta}: {e}")
                self.imagen = None

        def draw(self):
            if self.imagen:
                rect = self.imagen.get_rect(center=(int(self.pos.x), int(self.pos.y)))
                pantalla.blit(self.imagen, rect)
            else:
                pygame.draw.circle(pantalla, self.color, self.pos, self.r)
    

    s1=Sphere(40, color1, img1_path)
    s2=Sphere(40, color2, img2_path)
    orbes = []
    
    clock = pygame.time.Clock()

    # Timer para generar orbes cada 2 segundos
    tiempo_vida = 0
    tiempo_ataque = 0
    tiempo_velocidad= 0

    TIEMPO_ENTRE_ORBES = 2000  # milisegundos = 2 segundos
    DURACION_BUFF = 7000
    ESPERA_EXTRA = 5000
    TIEMPO_ENTRE_VELOCIDAD = DURACION_BUFF + ESPERA_EXTRA

    clock=pygame.time.Clock()

    def dibujar_barras():
        bw, bh, m = 80, 10, 5
        bx = (ANCHO - (bw * 5 + m * 4)) // 2

        fuente = pygame.font.SysFont(None, 28)

        # Nombre y barras del Jugador 1
        nombre_texto1 = fuente.render(nombre1.upper(), True, color1)
        pantalla.blit(nombre_texto1, (ANCHO//2 - nombre_texto1.get_width()//2, 10))
        for i in range(s1.salud):
            pygame.draw.rect(pantalla, color1, (bx + i * (bw + m), 40, bw, bh))

        # Nombre y barras del Jugador 2
        nombre_texto2 = fuente.render(nombre2.upper(), True, color2)
        pantalla.blit(nombre_texto2, (ANCHO//2 - nombre_texto2.get_width()//2, 70))
        for i in range(s2.salud):
            pygame.draw.rect(pantalla, color2, (bx + i * (bw + m), 100, bw, bh))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        tiempo_actual = pygame.time.get_ticks()

        # ——— 1) Verificar si venció el cronómetro ———
        if not juego_terminado_por_tiempo and tiempo_actual >= fin_reloj:
            juego_terminado_por_tiempo = True

        # ——— 2) Calcular texto del cronómetro “MM:SS” ———
        ms_restantes = max(0, fin_reloj - tiempo_actual)
        segundos_totales = ms_restantes // 1000
        minutos_display = segundos_totales // 60
        segundos_display = segundos_totales % 60
        texto_tiempo = f"{minutos_display:02d}:{segundos_display:02d}"

        # ——— 3) Si NO terminó el tiempo, ejecuto toda la lógica del juego ———
        if not juego_terminado_por_tiempo:
            # 3.1) Generación de orbes de vida y ataque
            hay_orbe_vida = any(o.tipo == 'vida' for o in orbes)
            if not hay_orbe_vida and tiempo_actual - tiempo_vida > TIEMPO_ENTRE_ORBES:
                orbes.append(Orb((0,255,0), 'vida'))
                tiempo_vida = tiempo_actual

            hay_orbe_ataque = any(o.tipo == 'ataque' for o in orbes)
            if not hay_orbe_ataque and tiempo_actual - tiempo_ataque > TIEMPO_ENTRE_ORBES:
                orbes.append(Orb((255,0,0), 'ataque'))
                tiempo_ataque = tiempo_actual

            # 3.2) Generación de orbe de velocidad
            hay_orbe_velocidad = any(o.tipo == 'velocidad' for o in orbes)
            buff_activo = (s1.vel_timer is not None) or (s2.vel_timer is not None)
            if (not hay_orbe_velocidad
                and not buff_activo
                and tiempo_actual - tiempo_velocidad > TIEMPO_ENTRE_VELOCIDAD):
                orbes.append(Orb((0,0,255), 'velocidad'))
                tiempo_velocidad = tiempo_actual

            # 3.3) Física de esferas
            collide(s1, s2)
            s1.move(); s2.move()
            s1.bounce_walls(); s2.bounce_walls()

            # 3.4) Restaurar velocidad tras buff de 7 s
            if s1.vel_timer and tiempo_actual - s1.vel_timer > DURACION_BUFF:
                s1.reset_velocidad()
                tiempo_velocidad = tiempo_actual - ESPERA_EXTRA
            if s2.vel_timer and tiempo_actual - s2.vel_timer > DURACION_BUFF:
                s2.reset_velocidad()
                tiempo_velocidad = tiempo_actual - ESPERA_EXTRA

            # 3.5) Mantener halo rápido si aún dura el buff
            if s1.vel_timer is not None:
                s1.halo_color = sphere_color_fast
            if s2.vel_timer is not None:
                s2.halo_color = sphere_color_fast

            # 3.6) Actualizar colores HSV para bordes y halos
            hue = (hue + hue_speed) % 1.0
            rgb_frac = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            border_color = tuple(int(c * 255) for c in rgb_frac)

            sphere_hue = (sphere_hue + sphere_hue_speed) % 1.0
            sphere_rgb = colorsys.hsv_to_rgb(sphere_hue, 1.0, 1.0)
            sphere_color_fast = tuple(int(c * 255) for c in sphere_rgb)

            # 3.7) Dibujar fondo, rectángulo de batalla y esferas
            pantalla.fill(NEGRO)
            pygame.draw.rect(pantalla, border_color, battle_rect, 2)
            s1.draw(); s2.draw()

            # 3.8) Dibujar y recoger orbes
            rem = []
            for o in orbes:

                o.draw()
                if o.tipo == 'vida' and s1.pos.distance_to(o.pos) < s1.r + o.r:
                    if s1.salud < 5:
                        s1.change_health(1)
                        sonido_vida.play()
                    rem.append(o)
                if o.tipo == 'vida' and s2.pos.distance_to(o.pos) < s2.r + o.r:
                    if s2.salud < 5:
                        s2.change_health(1)
                        sonido_vida.play()
                        rem.append(o)
                if o.tipo == 'ataque' and s1.pos.distance_to(o.pos) < s1.r + o.r:
                    s1.grab_orb_damage(o)
                    s1.has_attacked = False
                    sonido_katana.play()
                    rem.append(o)
                if o.tipo == 'ataque' and s2.pos.distance_to(o.pos) < s2.r + o.r:
                    s2.grab_orb_damage(o)
                    s2.has_attacked = False
                    sonido_katana.play()
                    rem.append(o)
                if o.tipo == "velocidad":
                    colision_s1 = s1.pos.distance_to(o.pos) < s1.r + o.r
                    colision_s2 = s2.pos.distance_to(o.pos) < s2.r + o.r
                    if colision_s1 or colision_s2:
                        s1.vel *= 2.5
                        s2.vel *= 2.5
                        s1.vel_timer = tiempo_actual
                        s2.vel_timer = tiempo_actual
                        rem.append(o)
            for o in rem:
                orbes.remove(o)

        
            dibujar_barras()


            if s1.salud <= 0 or s2.salud <= 0:
                centro_explosion = s1.pos if s1.salud <= 0 else s2.pos
                explosion(pantalla, clock, centro_explosion)
                pygame.time.wait(2000)
                return
      
        else:
            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            pantalla.blit(overlay, (0, 0))

            fuente_empate = pygame.font.SysFont(None, 72)
            texto_empate = fuente_empate.render("¡EMPATE!", True, (255, 255, 255))
            pantalla.blit(
                texto_empate,
                (
                    (ANCHO - texto_empate.get_width()) // 2,
                    (ALTO - texto_empate.get_height()) // 2
                )
            )

        fuente_tiempo = pygame.font.SysFont(None, 48)
        render_tiempo = fuente_tiempo.render(texto_tiempo, True, (255,255,255))
        pantalla.blit(render_tiempo, ((ANCHO - render_tiempo.get_width()) // 2, 140))

        pygame.display.flip()
        clock.tick(60)
    

if __name__ == "__main__":

    while True:
        n1, n2, c1, c2, img1, img2, tiempo_min = menu_configuracion()
        iniciar_juego(n1, n2, c1, c2, img1, img2, tiempo_min)