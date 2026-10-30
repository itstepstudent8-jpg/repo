from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Пересоздаем окно под дневную атмосферу
window.color = color.rgb(135, 206, 235)

game_state = 'menu'
inventory_open = False

# Список текстур и цветов блоков
textures = [
    load_texture('white_cube'),    # 0: Белый блок
    load_texture('brick'),         # 1: Кирпич
    load_texture('grass'),         # 2: Трава
    load_texture('white_cube'),    # 3: Стекло
    load_texture('white_cube'),    # 4: Дверь
    load_texture('white_cube')     # 5: Кровать
]

block_colors = [
    color.white,
    color.orange,
    color.green,
    color.rgba(200, 230, 255, 180), # Полупрозрачное стекло
    color.rgb(139, 69, 19),        # Коричневая дверь
    color.rgb(220, 20, 60)         # Красная кровать
]

block_names = ['Белый блок', 'Кирпич', 'Трава', 'Стекло', 'Дверь', 'Кровать']
current_texture = 2 # По умолчанию трава

class Voxel(Button):
    def __init__(self, position=(0,0,0), block_id=2):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            color=block_colors[block_id],
            texture=textures[block_id],
            scale=1
        )
        self.block_id = block_id

    def input(self, key):
        if self.hovered and not inventory_open:
            if key == 'left mouse down':
                Voxel(position=self.position + mouse.normal, block_id=current_texture)
            elif key == 'right mouse down':
                if self.y > 0:
                    destroy(self)

def generate_world():
    for z in range(20):
        for x in range(20):
            Voxel(position=(x, 0, z), block_id=2)

player = FirstPersonController()
player.disable()
player.x = 10
player.y = 5
player.z = 10

# --- Скайбокс: Дневное небо ---
sky = Sky(color=color.rgb(100, 180, 255))

# --- ГЛАВНОЕ МЕНЮ ---
menu_elements = []

def start_game():
    global game_state
    game_state = 'game'
    for e in menu_elements:
        e.disable()
    player.enable()
    generate_world()

title = Text(text='MINECRAFT PYTHON', scale=3, origin=(0, 0), y=0.3, color=color.gold, parent=camera.ui)
menu_elements.append(title)

play_btn = Button(text='ИГРАТЬ', color=color.azure, scale=(0.3, 0.1), y=0.0, parent=camera.ui, on_click=start_game)
menu_elements.append(play_btn)

quit_btn = Button(text='ВЫХОД', color=color.red, scale=(0.3, 0.1), y=-0.15, parent=camera.ui, on_click=application.quit)
menu_elements.append(quit_btn)

# --- ИНВЕНТАРЬ И UI ---
hotbar_text = Text(text='Блок: Трава (3) | [Q] Инвентарь', position=(-0.85, 0.45), scale=1.1, color=color.yellow)
hotbar_text.disable()

# Полупрозрачный фон для инвентаря
inventory_bg = Entity(parent=camera.ui, model='quad', scale=(0.6, 0.7), color=color.rgba(0, 0, 0, 200))
inventory_bg.disable()

inventory_title = Text(text='ИНВЕНТАРЬ БЛОКОВ', parent=camera.ui, scale=1.5, origin=(0,0), y=0.25, color=color.white)
inventory_title.disable()

inventory_buttons = []

def select_block_from_inv(index):
    global current_texture
    current_texture = index
    hotbar_text.text = f'Блок: {block_names[current_texture]} ({index+1}) | [Q] Инвентарь'
    toggle_inventory()

# Создаем слоты в инвентаре для каждого блока
for i, name in enumerate(block_names):
    btn = Button(
        parent=camera.ui,
        text=f'{i+1}. {name}',
        color=color.dark_gray,
        scale=(0.4, 0.08),
        y=0.15 - (i * 0.1),
        on_click=Func(select_block_from_inv, i)
    )
    btn.disable()
    inventory_buttons.append(btn)

def toggle_inventory():
    global inventory_open
    inventory_open = not inventory_open
    
    if inventory_open:
        player.disable()
        mouse.locked = False
        inventory_bg.enable()
        inventory_title.enable()
        for b in inventory_buttons:
            b.enable()
    else:
        player.enable()
        mouse.locked = True
        inventory_bg.disable()
        inventory_title.disable()
        for b in inventory_buttons:
            b.disable()

def update():
    global current_texture
    
    if game_state == 'game':
        hotbar_text.enable()
        
        # Открытие/закрытие инвентаря на клавишу Q
        if held_keys['q'] and not held_keys.get('debounce_q', False):
            held_keys['debounce_q'] = True
            toggle_inventory()
        elif not held_keys['q']:
            held_keys['debounce_q'] = False
            
        # Если инвентарь закрыт, работают цифры для быстрого выбора
        if not inventory_open:
            for i in range(1, 7):
                if held_keys[str(i)]:
                    current_texture = i - 1
                    hotbar_text.text = f'Блок: {block_names[current_texture]} ({i}) | [Q] Инвентарь'
                    
        if held_keys['escape'] and not inventory_open:
            application.quit()

app.run()