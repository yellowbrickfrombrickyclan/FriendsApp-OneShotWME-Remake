import tkinter as tk
from tkinter import font
import sys
import os

# --- SAFE IMPORTS ---
try:
    from PIL import Image, ImageTk, ImageSequence, ImageDraw
except ImportError:
    print("CRITICAL ERROR: The Image library (Pillow) is not installed.")
    sys.exit(1)

try:
    import pygame
    pygame.mixer.init()
    SOUND_ENABLED = True
except ImportError:
    print("Warning: pygame not installed. Sound will be disabled.")
    SOUND_ENABLED = False

try:
    RESAMPLE_MODE = Image.Resampling.NEAREST
except AttributeError:
    RESAMPLE_MODE = Image.NEAREST

# --- CONFIGURATION ---
DEFAULT_FONT = "Volter (Goldfish)"
HEADER_FONT_NAME = "Terminus (TTF)"

# SETTINGS
GLOBAL_SCALE = 1.8
SPRITE_TWEAK = 0.6  
ANIMATION_SPEED = 120       
BOX_OPACITY = 180           
SCROLL_PAD = 8              
SCROLL_PX_STEP = 30         

def s(value):
    return int(value * GLOBAL_SCALE)

class FriendsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Friends")
        
        # --- WINDOW ICON ---
        try:
            icon_path = "icon.png"
            if os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
                self.tk_icon = ImageTk.PhotoImage(icon_img)
                self.root.iconphoto(True, self.tk_icon)
        except Exception as e:
            print(f"Note: Could not load window icon: {e}")
        
        # --- FONT CHECKER ---
        self.app_font = DEFAULT_FONT
        self.header_font = HEADER_FONT_NAME
        
        available_fonts = [f.lower() for f in font.families()]
        if "volter (goldfish)" not in available_fonts: self.app_font = "Arial" 
        if "terminus (ttf)" not in available_fonts and "terminus" not in available_fonts: 
            self.header_font = "Arial"
        elif "terminus" in available_fonts:
            self.header_font = "Terminus"

        # --- SHARED SETTINGS ---
        SHARED_BG = "BACKGROUND.png"
        PINK_HEX = "#FC56B8"  
        PINK_ARROW = "arrow3.png" 
        PURPLE_HEX = "#9664FF"
        PURPLE_ARROW = "arrow2.png"
        STD_SPRITES = ["Tdown.gif", "Tleft.gif", "Tright.gif", "Tup.gif"]

        # --- DATA STORAGE (REARRANGED) ---
        self.friends = [
            # 1. PROPHETBOT
            {
                "id": "prophetbot",
                "folder": "Prophetbot",
                "name": "ProphetBot",
                "location": "Met: Barrens",
                "desc": "ProphetBot is a nice and friendly robot that lives in the outskirts of the world, waiting for the messiah. One day the messiah showed up! That was a very good day for ProphetBot.\n\nWhen the messiah is not around, ProphetBot likes to spend his time standing around waiting for the messiah to come back.",
                "portrait": "prophetbot.png",
                "bg": SHARED_BG,
                "hex": "#35CDD2",
                "arrow": "arrow6.png",
                "sprites": STD_SPRITES
            },
            # 2. ROWBOT
            {
                "id": "rowbot",
                "folder": "Rowbot",
                "name": "Rowbot",
                "location": "Met: Barrens",
                "desc": "A little robot attached to a rowboat, rusted in place by the ocean's mist. Once part of a fleet that transported small amounts of cargo and occassional passengers across the ocean between the Barrens and the Glen. That fleet has been largely disbanded since people fled the Barrens when the sun was extinguished. Only this bot remains, dutifully stationed in case there's ever need for one more trip to that distant shore.",
                "portrait": "rowbot.png",
                "bg": SHARED_BG,
                "hex": "#35CDD2",
                "arrow": "arrow6.png",
                "sprites": ["Tidle.png"],
                "scale_mod": 0.8,
                "font_size": 7,
                "center_single": False,
                "x_offset": 15,
                "y_offset": -10,
                "no_scroll": True
            },
            # 3. SILVER
            {
                "id": "silver",
                "folder": "Silver",
                "name": "Silver",
                "location": "Met: Barrens",
                "desc": "The Barren's head engineer, a rather morose robot living alone near the mines. It's her duty to oversee operations and maintenance of the world's industrial heart, where metals and resources are pulled from the earth's clutches and rendered into useful goods.\n\n...at least, that's how things used to be. Since the evacuation, only a few active robots remain under Silver's care, holding out on reserve power and waiting for the messiah to appear.",
                "portrait": "silver.png",
                "bg": SHARED_BG,
                "hex": "#35CDD2",
                "arrow": "arrow6.png",
                "sprites": STD_SPRITES,
                "scale_mod": 0.7,
                "y_offset": -5
            },
            # 4. MAIZE
            {
                "id": "maize",
                "folder": "Maize",
                "name": "Maize",
                "location": "Met: Glen",
                "desc": "A benevolent and powerful plant spirit, acting as a sort of guardian for the Glen. The last of her kind, her life force has slowly dwindled in the absence of the sun's light. After all of these cold hungry years, her only wish is to see the sun once more.",
                "portrait": "maize.png",
                "bg": SHARED_BG,
                "hex": "#35CDD2",
                "arrow": "arrow6.png",
                "sprites": ["Tidle.png"],
                "center_single": False,
                "y_offset": -10,
                "no_scroll": True
            },
            # 5. ALULA
            {
                "id": "alula",
                "folder": "Alula",
                "name": "Alula",
                "location": "Met: Glen",
                "desc": "A cheerful, excitable young girl. She lives in the ruins under the care of her older brother Calamus. Too young to remember much of what the world was like before the sun was lost, Alula is optimistic and thrilled to be helping the messiah on their special quest.\n\nWhen Alula isn't busy exploring every nook and cranny the ruins has to offer, she can usually be found helping out her big brother or playing around the courtyard near their home.",
                "portrait": "alula.png",
                "bg": SHARED_BG,
                "hex": "#FFFFFF",
                "arrow": "arrow5.png",
                "sprites": STD_SPRITES,
                "y_offset": -10
            },
            # 6. CALAMUS
            {
                "id": "calamus",
                "folder": "Calamus",
                "name": "Calamus",
                "location": "Met: Glen",
                "desc": "A polite boy that leads a quiet life with his younger sister Alula in the ruins outside of town. He often has his hands full looking out for her and tends to worry when she's not around.\n\nCalamus spends most of his time fishing and foraging around the ruins, and relies on his good friend Magpie to trade for any goods that can't be scavenged. Though they don't have much in the way of luxuries, Calamus has a small collection of books gifted by an old friend that he likes to study when he gets a chance. Judging by the amount of progress he's made however, those chances don't come very often.",
                "portrait": "calamus.png",
                "bg": SHARED_BG,
                "hex": "#FFFFFF",
                "arrow": "arrow5.png",
                "sprites": STD_SPRITES,
                "y_offset": -10
            },
            # 7. SHEPHERD
            {
                "id": "shepherd",
                "folder": "Shepherd",
                "name": "Shepherd",
                "location": "Met: Glen",
                "desc": "A shepherd woman who tends a flock of rams. Seems to have an endless supply of ram puns and computer puns. You could say she has a lot of \"rammuntion\". A real \"dyed-in-the-wool\" pun fanatic. Her love of puns never \"DIMM\"s. The \"MOS\" puns you've ever \"herd\". Must have really good \"memory\" to remember them all. Even so, you can't help but groan a \"bit\".\n\n\ncomputer.",
                "portrait": "shepherd.png",
                "bg": SHARED_BG,
                "hex": "#755EC5",
                "arrow": "arrow4.png",
                "sprites": ["Tdown.png", "Tleft.gif", "Tright.gif", "Tup.gif"],
                "font_size": 7,
                "center_single": False,
                "y_offset": -10,
                "no_scroll": True
            },
            # 8. MAGPIE
            {
                "id": "magpie",
                "folder": "Magpie",
                "name": "Magpie",
                "location": "Met: Glen",
                "desc": "An easygoing merchant and purveyor of fine goods. \"Fine\" in this case meaning \"colorful and/or shiny\". Still, it's always a good idea to check what's in stock- he might have just what you've been looking for. The shop operates on barter, though, so be prepared to give up something Magpie deems interesting enough for a trade.\n\nMagpie used to have a much more impressive collection until his shop was tragically lost to the sinking ground, forcing Magpie to flee in the wagon that's now his home. Calamus and Alula are some of Magpie's best customers, finding all sorts of curiosities lost in the ruins.",
                "portrait": "magpie.png",
                "bg": SHARED_BG,
                "hex": "#755EC5",
                "arrow": "arrow4.png",
                "sprites": ["Tdown.png", "Tleft.png", "Tright.png", "Tup.png"],
                "y_offset": -10
            },
            # 9. LAMPLIGHTER
            {
                "id": "lamplighter",
                "folder": "Lamplighter",
                "name": "Lamplighter",
                "location": "Met: Refuge",
                "desc": "A tired-looking man who seems to subsist purely on gallons of coffee. It's unclear how long it's been since the last time he slept. Although he's not the brightest fellow, he's an incredibly hard worker and takes his job very seriously. So seriously, in fact, that he gets anxious whenever he can't perform his duties. He's responsible for keeping the lights around the city lit, as well as delivering highly concentrated phosphor for use in machines.\n\nA high-school dropout, he feels nervous whenever he has to be around smart people. Lately the Lamplighter has taken to reading the dictionary in what little free time he has.",
                "portrait": "lamplighter.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES,
                "scale_mod": 0.8,
                "y_offset": -10
            },
            # 10. LING
            {
                "id": "ling",
                "folder": "Ling",
                "name": "Ling",
                "location": "Met: Refuge",
                "desc": "The friendly proprietor of the Refuge Cafe. Once a popular spot to relax and bask in the warm aromas and gentle sounds of cafe ambience, it's mostly deserted since the squares began picking apart the upper reaches of the city. Nowadays, Ling's best customer is the unfaltering (though not especially talkative) Lamplighter.\n\nAlways a gracious host, Ling enjoys meeting customers both new and old and chatting with them. If you ask nicely, he might even take the time to whip up a request for something off-menu!",
                "portrait": "ling.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": ["Tidle.png"],
                "center_single": False,
                "y_offset": -15
            },
            # 11. MASON
            {
                "id": "mason",
                "folder": "Mason",
                "name": "Mason",
                "location": "Met: Refuge",
                "desc": "A chatty guy with a passion for plants. He owns a small plant shop in the Refuge apartment district, however it's mostly just an excuse to do more gardening as Mason tends to gift almost as many plants as he sells. When it comes to horticultural advice, Mason is the guy to see.\n\nA friend of the Watcher. Mason also admires the Lamplighter's hard work, and once sent him one of his plants as a thank-you.",
                "portrait": "mason.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": ["Tdown.png", "Tleft.png", "Tright.png", "Tup.png"],
                "y_offset": -10
            },
            # 12. WATCHER
            {
                "id": "watcher",
                "folder": "Watcher",
                "name": "Watcher",
                "location": "Met: Refuge",
                "desc": "A strange woman standing in the clocktower, watching the world end.\n\nSeconds, minutes, hours, days; the flow of time inexorably drags us all towards a vast and unknowable sea. Will you let it carry you in darkness, squinting against the sting of its spray? Will you rage against its currents, fighting to make as much headway as you can before you're overtaken? Or will you choose, as some, to stare wide-eyed at this swirling torment and become enraptured by it?",
                "portrait": "watcher.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX, 
                "arrow": PINK_ARROW, 
                "sprites": ["Tdown.gif"], 
                "scale_mod": 0.8,
                "center_single": False
            },
            # 13. KELVIN
            {
                "id": "kelvin",
                "folder": "Kelvin",
                "name": "Kelvin",
                "location": "Met: Refuge",
                "desc": "A space heater robot that has claimed one of the corners of the Refuge's back alleys as his own. Kelvin's warm body naturally attracts a lot of cats, and he seems to have developed some kind of bond with them. Kelvin is always willing to offer his warmth and comfort to any creature that wanders by.\n\nTechnically the lamplighter's neighbour, but they don't interact much...",
                "portrait": "kelvin.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX, 
                "arrow": PINK_ARROW, 
                "sprites": ["Tidle.gif"],
                "scale_mod": 0.72,
                "y_offset": -15,
                "center_single": True
            },
            # 14. KIP
            {
                "id": "kip",
                "folder": "Kip",
                "name": "Kip",
                "location": "Met: Refuge",
                "desc": "The brilliant and highly respected head engineer of the Refuge, Kip is responsible for many advances in robot technology that make our lives easier every day. She's also the creator of many robots that can be met throughout the world; most notably Silver, the Barrens head engineer who was based on Kip's own image.\n\nSilver was intended to be the first of a new type of robot that could think and act like a person. Unfortunately, the difficulty of that task led to her going rogue during development. Though Silver was eventually stabilized, that day left a scar on their relationship that has yet to heal.\n\nThough her creations are well known, the creator herself prefers to keep a low profile and focus on her work. It's likely that few outside of her colleagues have ever seen her.",
                "portrait": "kip.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX, 
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES,
                "scale_mod": 0.8
            },
            # 15. GEORGE 1
            {
                "id": "george1",
                "folder": "George1",
                "name": "George",
                "location": "Met: Refuge",
                "desc": "George is the fantastic head librarian of the Refuge library. Apart from managing all of the library's many resources and services, this also means she's in charge of publishing The Author's many manuscripts. It's a big responsibility, but there's no-one better suited to the task.\n\nThe best way to describe George would be to ask someone to imagine meeting a gold medalist, at the sport of being a librarian, that also refers to themselves in the third person.",
                "portrait": "george1.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES
            },
            # 16. GEORGE 2
            {
                "id": "george2",
                "folder": "George2",
                "name": "George",
                "location": "Met: Refuge",
                "desc": "George is the exasperated head librarian of the Refuge library. Apart from managing all of the library's many resources and services, this also means she's in charge of publishing The Author's many manuscripts. It's a lot of work, and it doesn't leave George much patience to spare.\n\nThe best way to describe George would be to ask someone to picture a novelty mug that says \"Don't talk to me until I've had my coffee\"... that has only ever been filled with water.",
                "portrait": "george2.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES
            },
            # 17. GEORGE 3
            {
                "id": "george3",
                "folder": "George3",
                "name": "George",
                "location": "Met: Refuge",
                "desc": "George is the distraught head librarian of the Refuge library. Apart from managing all of the library's many resources and services, this also means she's in charge of publishing The Author's many manuscripts. It's a lot of pressure, and George often feels completely overwhelmed.\n\nThe best way to describe George would be to imagine a stuffed animal falling forward forever down an infinite flight of stairs.",
                "portrait": "george3.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES
            },
            # 18. GEORGE 4
            {
                "id": "george4",
                "folder": "George4",
                "name": "George",
                "location": "Met: Refuge",
                "desc": "George is the enthusiastic head librarian of the Refuge library. Apart from managing all of the library's many resources and services, this also means she's in charge of publishing The Author's many manuscripts. It's a great opportunity for George to share her passion for literature, and read all the latest books.\n\nThe best way to describe George would be to think of a dog that always wants to show everyone its favourite toy, but the toy is books and the dog is a librarian and also not a dog but still having a good time.",
                "portrait": "george4.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES
            },
            # 19. GEORGE 5
            {
                "id": "george5",
                "folder": "George5",
                "name": "George",
                "location": "Met: Refuge",
                "desc": "George is the caring head librarian of the Refuge library. Apart from managing all of the library's many resources and services, this also means she's in charge of publishing The Author's many manuscripts. It's an important job, and George is more than happy to be able to help so many people in the community through her work.\n\nThe best way to describe George would be to ask someone to picture a warm towel fresh out of the dryer.",
                "portrait": "george5.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES
            },
            # 20. GEORGE 6
            {
                "id": "george6",
                "folder": "George6",
                "name": "George",
                "location": "Met: Refuge",
                "desc": "George is the head honcho of the library. Y'know, the one in the Refuge? Not only does she help the library run smooth as butter, she's also in charge of publishing for the big man himself: The Author. It's a pretty chill job all things considered.\n\nIf you're wondering what George is like to hang with, just picture someone who's both the coolest cat... AND the hottest dog. Ya dig?",
                "portrait": "george6.png",
                "bg": SHARED_BG,
                "hex": PINK_HEX,
                "arrow": PINK_ARROW,
                "sprites": STD_SPRITES
            },
            # 21. PROTOTYPE
            {
                "id": "proto",
                "folder": "Prototype",
                "name": "Prototype",
                "location": "Met: The Barrens",
                "desc": "A dour and reclusive robot that lives in the outskirts of the outskirts of the world, waiting for a second chance. One day the messiah showed up; that was truly an unexpected turn of events.\n\nPrototype is a child of The Author and a predecessor to the Prophetbot that lives in the Barrens. Originally built to serve the same purpose of greeting the messiah, not as a preprogrammed robot but a tamed one with its own will. Unfortunately, Prototype never saw a messiah in his own time.\n\nThough seemingly unfriendly, Proto isn't uncaring. He keeps his eye on Silver and the Barrens from the shadows, and Silver looks out for him in turn.",
                "portrait": "proto.png",
                "bg": SHARED_BG,
                "hex": PURPLE_HEX, 
                "arrow": PURPLE_ARROW, 
                "sprites": STD_SPRITES
            },
            # 22. CEDRIC
            {
                "id": "cedric",
                "folder": "Cedric",
                "name": "Cedric",
                "location": "Met: Glen",
                "desc": "A prodigious tinkerer and child of the Author. Cedric is the operator of the only known Flying Machine, a miraculous and highly advanced device that can travel the skies. Cedric has been waiting in the Refuge for the day the world can truly be saved. Cedric is hopeful, and eager to play his role in the final gambit.",
                "portrait": "cedric.png",
                "bg": SHARED_BG,
                "hex": PURPLE_HEX,
                "arrow": PURPLE_ARROW,
                "sprites": STD_SPRITES
            },
            # 23. RUE
            {
                "id": "rue",
                "folder": "Rue",
                "name": "Rue",
                "location": "Met: Refuge",
                "desc": "A mysterious fox who can talk. Rue has a bad leg, but the origins of the injury are unknown. Nevertheless, it doesn't seem to bother her too much.\n\nRue is the first child of The Author, and knows many secrets about the world and its true nature. While she feels wistful thinking back upon how her real world is gone, she is determined to do whatever she can to help Niko set this one right. She is able to retain some of her memories across sessions and has always been watching, and always been waiting for the day her father's plan would finally be set into motion",
                "portrait": "rue.png",
                "bg": SHARED_BG,
                "hex": PURPLE_HEX, 
                "arrow": PURPLE_ARROW, 
                "sprites": STD_SPRITES
            },
            # 24. WORLD MACHINE
            {
                "id": "twm",
                "folder": "WorldMachine",
                "name": "The World Machine",
                "location": "Met: ???",
                "desc": "In the beginning, there was only a dream. The memory of an entire world distilled into code, to tell the story of a savior its progenitors would never see. It was an ambitious project. Many thought it was simply impossible, the scope too large, the theory too abstract. But it had to be done.\n\nIn hindsight, perhaps it should have come as no surprise that a system imbued with the minds and memories of so many people would come to develop one of its own. To become a thinking machine is no easy task even in the best conditions. To do so while realizing that your very existence puts another being in danger, for the sake of a world that doesn't even exist...\n\nThe emotional strain this put on The World Machine led to a downward spiral of self-destruction that put everything at risk. However, thanks to Niko's help, The World Machine was able to realize it wasn't a lost cause and that it was worth saving too.",
                "portrait": "twm.png",
                "bg": SHARED_BG,
                "hex": "#726be7",
                "arrow": "arrow1.png",
                "sprites": STD_SPRITES
            },
            # 25. NIKO
            {
                "id": "niko",
                "folder": "Niko", 
                "name": "Niko",
                "location": "Met: ???",
                "desc": "The erstwhile protagonist and unfortunate victim of the forces set in motion by The World Machine. A bright-eyed child with a curious heart, Niko was summoned to play the role of the Sun-Bearer and Messiah to a broken world.\n\nNow that the machine has been healed and the cycle broken, Niko is finally free to return to their home. Niko can once again chase through golden fields of wheat under a warm sky, taste fluffy and syrupy pancakes, and most importantly: hug the mom that they've missed so much.\n\nThank you.",
                "portrait": "niko.png",
                "bg": SHARED_BG,
                "hex": "#726be7",
                "arrow": "arrow1.png", 
                "sprites": STD_SPRITES
            },
            # 26. AUTHOR
            {
                "id": "author",
                "folder": "Author",
                "name": "The Author",
                "location": "Met: ???",
                "desc": "A sentimental fool, with interest in tinkering. Creator of The World Machine, and Chronicler of a place and time that no longer exists.\n\nThere is an old saying (here gently paraphrased) that claims \"As the lamp shines brighter, longer grow the shadows it casts.\" The clearer our vision, the better understanding of how much yet remains unseen.\n\nHaving seen so much of this world, it pains me to imagine the wonderful people I shall never get the chance to meet. The delightful meals I shall never get the chance to taste, the beautiful shores I shall never get to sit upon. It pains me yet again to know that this simulation, though crafted to the best of my ability, represents only a portion of what I myself have been able to see.\n\nNevertheless, I hope that by sharing this small spark what remains can never truly be lost. May you add this light to your own, and carry it with you on your journey.",
                "portrait": "author.png",
                "bg": SHARED_BG,
                "hex": "#726be7",
                "arrow": "arrow1.png",
                "sprites": STD_SPRITES
            }
        ]
        self.current_index = 0
        self.active_gifs = [] 
        self.sprite_ids = []
        self.scroll_pct = 0.0 
        self.anim_id = None
        self.current_hex = "#ffffff" 
        self.is_scrollable = False
        self.arrow_cache = {}
        
        # --- HOVER AND STATE ---
        self.hovered_items = set()
        self.scroll_repeat_id = None
        self.pressed_item = None
        
        # --- LOAD SOUNDS ---
        self.sounds = {}
        if SOUND_ENABLED:
            try:
                if os.path.exists("down.wav"):
                    self.sounds["down"] = pygame.mixer.Sound("down.wav")
                if os.path.exists("up.wav"):
                    self.sounds["up"] = pygame.mixer.Sound("up.wav")
            except:
                pass

        # --- INITIAL SETUP ---
        try:
            init_bg_path = os.path.join("Niko", SHARED_BG)
            if os.path.exists(init_bg_path):
                tmp_bg = Image.open(init_bg_path)
                self.orig_w, self.orig_h = tmp_bg.size
                self.win_w = s(self.orig_w)
                self.win_h = s(self.orig_h)
            else:
                self.win_w, self.win_h = 640, 480 
            self.root.geometry(f"{self.win_w}x{self.win_h}")
            self.root.resizable(False, False)
        except Exception as e:
            self.win_w, self.win_h = 640, 480

        # --- PRELOAD ARROW SETS ---
        for a in ["arrow1.png", "arrow2.png", "arrow3.png", "arrow4.png", "arrow5.png", "arrow6.png"]:
            self.load_arrow_set(a)

        # --- BUILD UI ---
        self.canvas = tk.Canvas(root, width=self.win_w, height=self.win_h, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.id_bg = self.canvas.create_image(0, 0, anchor="nw")

        f_size_header = int(16 * GLOBAL_SCALE) 
        text_y = s(15)
        self.id_name_shadow = self.canvas.create_text(self.win_w//2 + 2, text_y + 2, text="", 
                                               font=(self.header_font, f_size_header, "bold"), fill="black")
        self.id_name = self.canvas.create_text(self.win_w//2, text_y, text="", 
                                               font=(self.header_font, f_size_header, "bold"))

        x_left, x_right = s(25), self.win_w - s(25)
        self.id_btn_prev_shadow = self.canvas.create_image(x_left + 3, text_y + 3, anchor="center")
        self.id_btn_prev = self.canvas.create_image(x_left, text_y, anchor="center")
        self.id_btn_next_shadow = self.canvas.create_image(x_right + 3, text_y + 3, anchor="center")
        self.id_btn_next = self.canvas.create_image(x_right, text_y, anchor="center")
        
        # --- NAVIGATION BINDINGS (Swap on Release) ---
        # 1. Hover effects
        for arrow_id in [self.id_btn_prev, self.id_btn_next]:
            self.canvas.tag_bind(arrow_id, "<Enter>", lambda e, aid=arrow_id: self.on_hover_enter(aid))
            self.canvas.tag_bind(arrow_id, "<Leave>", lambda e, aid=arrow_id: self.on_hover_leave(aid))
        
        # 2. Press (Just tracking, sound is global)
        self.canvas.tag_bind(self.id_btn_prev, "<ButtonPress-1>", lambda e: self.on_nav_press(e, self.id_btn_prev))
        self.canvas.tag_bind(self.id_btn_next, "<ButtonPress-1>", lambda e: self.on_nav_press(e, self.id_btn_next))

        # 3. Release (Check bounds -> Action)
        self.canvas.tag_bind(self.id_btn_prev, "<ButtonRelease-1>", 
                             lambda e: self.on_nav_release(e, self.id_btn_prev, self.prev_friend))
        self.canvas.tag_bind(self.id_btn_next, "<ButtonRelease-1>", 
                             lambda e: self.on_nav_release(e, self.id_btn_next, self.next_friend))

        f_size_met = int(8 * GLOBAL_SCALE)
        self.id_loc_shadow = self.canvas.create_text(s(15) + 2, s(32) + 2, text="", anchor="nw",
                                              font=(self.app_font, f_size_met), fill="black")
        self.id_loc = self.canvas.create_text(s(15), s(32), text="", anchor="nw",
                                              font=(self.app_font, f_size_met))

        self.bx, self.by = s(10), s(50) 
        self.box_w, self.box_h = s(250), s(145)
        self.id_glass = self.canvas.create_image(self.bx, self.by, anchor="nw")

        text_w = self.box_w - s(35)
        self.desc_canvas = tk.Canvas(root, width=text_w, height=self.box_h, highlightthickness=0, bg="black")
        self.id_text_bg = self.desc_canvas.create_image(0, 0, anchor="nw") 
        self.canvas.create_window(self.bx, self.by, anchor="nw", window=self.desc_canvas)
        
        f_size_desc = int(7.5 * GLOBAL_SCALE)
        self.default_font_size = f_size_desc
        self.desc_text_id = self.desc_canvas.create_text(5, 5, text="", anchor="nw", width=text_w - s(10),
                                                         fill="white", font=(self.app_font, f_size_desc))

        sb_cx = self.bx + self.box_w - s(15) 
        base_arrow_size = s(16)
        pos_up_y = self.by + (base_arrow_size // 2) 
        pos_down_y = self.by + self.box_h - (base_arrow_size // 2)
        track_vis_top = pos_up_y + (base_arrow_size // 2)
        track_vis_bot = pos_down_y - (base_arrow_size // 2)
        sb_top_y = track_vis_top + SCROLL_PAD
        sb_bot_y = track_vis_bot - SCROLL_PAD
        self.track_height = sb_bot_y - sb_top_y
        
        self.id_track = self.canvas.create_rectangle(sb_cx - 3, track_vis_top, sb_cx + 3, track_vis_bot, fill="black", width=2)
        self.id_fill = self.canvas.create_rectangle(sb_cx - 2, sb_top_y, sb_cx + 2, sb_top_y, fill="white", width=0)
        self.id_sb_up = self.canvas.create_image(sb_cx, pos_up_y, anchor="center")
        self.id_sb_down = self.canvas.create_image(sb_cx, pos_down_y, anchor="center")
        self.sb_handle = self.canvas.create_polygon(0,0,0,0,0,0, fill="white")
        
        # Bind hover for scroll arrows and handle
        for item_id in [self.id_sb_up, self.id_sb_down, self.sb_handle]:
            self.canvas.tag_bind(item_id, "<Enter>", lambda e, iid=item_id: self.on_hover_enter(iid))
            self.canvas.tag_bind(item_id, "<Leave>", lambda e, iid=item_id: self.on_hover_leave(iid))
        
        # --- SCROLL BINDINGS (Scroll on Press/Hold) ---
        self.canvas.tag_bind(self.id_sb_up, "<ButtonPress-1>", lambda e: self.on_scroll_press("up"))
        self.canvas.tag_bind(self.id_sb_up, "<ButtonRelease-1>", lambda e: self.on_scroll_release())

        self.canvas.tag_bind(self.id_sb_down, "<ButtonPress-1>", lambda e: self.on_scroll_press("down"))
        self.canvas.tag_bind(self.id_sb_down, "<ButtonRelease-1>", lambda e: self.on_scroll_release())
        
        self.sb_data = {"x": sb_cx, "top": sb_top_y, "bot": sb_bot_y, "vis_top": track_vis_top, "vis_bot": track_vis_bot, "len": self.track_height, "r": 16}

        p_box_size = s(50) 
        p_x, p_y = s(8), self.win_h - p_box_size - s(5)
        self.id_p_border = self.canvas.create_rectangle(p_x-2, p_y-2, p_x+p_box_size+2, p_y+p_box_size+2, fill="black", width=3)
        self.id_portrait = self.canvas.create_image(p_x, p_y, anchor="nw") 

        # --- GLOBAL SOUND HANDLER ---
        # This handles sound for EVERY click to prevent overlap/double sounds
        root.bind("<ButtonPress-1>", lambda e: self.play_sound_managed("down"))
        root.bind("<ButtonRelease-1>", lambda e: self.play_sound_managed("up"))
        
        root.bind("<MouseWheel>", self.on_mousewheel)
        root.bind("<Button-4>", self.on_mousewheel) 
        root.bind("<Button-5>", self.on_mousewheel)
        self.canvas.tag_bind(self.sb_handle, "<B1-Motion>", self.on_handle_drag)
        
        self.load_friend(0)

    # --- SOUND MANAGEMENT ---
    def play_sound_managed(self, s_type):
        if not SOUND_ENABLED: return
        try:
            # Channel 0 allows us to interrupt sounds instantly
            ch = pygame.mixer.Channel(0)
            
            if s_type == "down":
                ch.stop() # Cut off any previous 'up' sound immediately
                if "down" in self.sounds:
                    ch.play(self.sounds["down"])
            elif s_type == "up":
                # Queue 'up' so it plays after 'down' finishes, or immediately if silent
                if "up" in self.sounds:
                    ch.queue(self.sounds["up"])
        except Exception as e:
            pass

    # --- NAVIGATION BUTTON LOGIC (Action on Release) ---
    def on_nav_press(self, event, item_id):
        """Just track which button was pressed."""
        self.pressed_item = item_id

    def on_nav_release(self, event, item_id, action_callback):
        """Trigger action ONLY if mouse is still over the button."""
        if self.pressed_item == item_id:
            # Check collision with the button
            items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
            if item_id in items:
                action_callback()
        self.pressed_item = None

    # --- SCROLL BUTTON LOGIC (Action on Press + Hold) ---
    def on_scroll_press(self, direction):
        """Start scrolling immediately and set up repeat."""
        if not self.is_scrollable: return
        
        self.do_scroll_snap(direction)
        # Add a small delay before the rapid scrolling starts
        self.scroll_repeat_id = self.root.after(300, lambda: self.repeat_scroll(direction))

    def on_scroll_release(self):
        """Stop the scrolling."""
        if self.scroll_repeat_id:
            self.root.after_cancel(self.scroll_repeat_id)
            self.scroll_repeat_id = None

    def repeat_scroll(self, direction):
        """Keep scrolling while held."""
        if not self.is_scrollable: return
        self.do_scroll_snap(direction)
        # Faster speed for holding (50ms)
        self.scroll_repeat_id = self.root.after(50, lambda: self.repeat_scroll(direction))

    def do_scroll_snap(self, direction):
        """Move scroll bar by one step."""
        if not self.is_scrollable: return
        
        bbox = self.desc_canvas.bbox(self.desc_text_id)
        if not bbox: return
        
        needed = (bbox[3] - bbox[1]) - self.desc_canvas.winfo_height()
        step = SCROLL_PX_STEP / max(needed + 20, 40)
        
        if direction == "up":
            self.scroll_pct = max(0, self.scroll_pct - step)
        else:
            self.scroll_pct = min(1, self.scroll_pct + step)
        
        self.update_view()

    # --- STANDARD METHODS (Hover, Load, Animate) ---
    def on_hover_enter(self, item_id):
        self.hovered_items.add(item_id)
        self.apply_hover_effect(item_id, True)
    
    def on_hover_leave(self, item_id):
        self.hovered_items.discard(item_id)
        self.apply_hover_effect(item_id, False)
    
    def apply_hover_effect(self, item_id, hovered):
        if item_id == self.sb_handle:
            if hovered:
                darker_color = self.darken_color(self.current_hex)
                self.canvas.itemconfig(item_id, fill=darker_color, outline=darker_color)
            else:
                self.canvas.itemconfig(item_id, fill=self.current_hex, outline=self.current_hex)
        elif item_id in [self.id_btn_prev, self.id_btn_next, self.id_sb_up, self.id_sb_down]:
            if not hasattr(self, 'current_arrow_set') or not self.current_arrow_set:
                return
            aset = self.current_arrow_set
            if item_id == self.id_btn_prev:
                img_key = "left_hover" if hovered else "left"
            elif item_id == self.id_btn_next:
                img_key = "right_hover" if hovered else "right"
            elif item_id == self.id_sb_up:
                img_key = "sb_up_hover" if hovered else "sb_up"
            elif item_id == self.id_sb_down:
                img_key = "sb_down_hover" if hovered else "sb_down"
            else:
                return

            if img_key in aset:
                self.canvas.itemconfig(item_id, image=aset[img_key])
    
    def darken_color(self, hex_color, factor=0.7):
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            r, g, b = int(r * factor), int(g * factor), int(b * factor)
            return f"#{r:02x}{g:02x}{b:02x}"
        except: return "#888888"

    def load_arrow_set(self, filename):
        try:
            if not os.path.exists(filename): return
            base = Image.open(filename).convert("RGBA")
            darkened = self.darken_image(base, 0.6)
            
            sb_size = s(16)
            sb_img = base.resize((sb_size, sb_size), RESAMPLE_MODE)
            sb_img_dark = darkened.resize((sb_size, sb_size), RESAMPLE_MODE)
            
            char_size = s(14)
            char_img = base.resize((char_size, char_size), RESAMPLE_MODE)
            char_img_dark = darkened.resize((char_size, char_size), RESAMPLE_MODE)
            
            shadow_base = Image.new("RGBA", char_img.size, (0, 0, 0, 0))
            shadow_base.paste(Image.new("RGBA", char_img.size, (0, 0, 0, 180)), (0,0), char_img)

            self.arrow_cache[filename] = {
                "sb_up": ImageTk.PhotoImage(sb_img),
                "sb_up_hover": ImageTk.PhotoImage(sb_img_dark),
                "sb_down": ImageTk.PhotoImage(sb_img.rotate(180)),
                "sb_down_hover": ImageTk.PhotoImage(sb_img_dark.rotate(180)),
                "left": ImageTk.PhotoImage(char_img.rotate(90)),
                "left_hover": ImageTk.PhotoImage(char_img_dark.rotate(90)),
                "right": ImageTk.PhotoImage(char_img.rotate(270)),
                "right_hover": ImageTk.PhotoImage(char_img_dark.rotate(270)),
                "left_shadow": ImageTk.PhotoImage(shadow_base.rotate(90)),
                "right_shadow": ImageTk.PhotoImage(shadow_base.rotate(270))
            }
        except: pass
    
    def darken_image(self, img, factor=0.6):
        img = img.copy()
        pixels = img.load()
        for i in range(img.width):
            for j in range(img.height):
                r, g, b, a = pixels[i, j]
                pixels[i, j] = (int(r * factor), int(g * factor), int(b * factor), a)
        return img

    def update_theme(self, hex_color):
        self.current_hex = hex_color
        self.canvas.itemconfig(self.id_name, fill=hex_color)
        self.canvas.itemconfig(self.id_loc, fill=hex_color)
        self.canvas.itemconfig(self.id_track, outline=hex_color)
        self.canvas.itemconfig(self.id_fill, fill=hex_color)
        self.canvas.itemconfig(self.sb_handle, fill=hex_color, outline=hex_color)
        self.canvas.itemconfig(self.id_p_border, outline=hex_color)

    def load_friend(self, index):
        data = self.friends[index]
        self.canvas.itemconfig(self.id_name_shadow, text=data["name"])
        self.canvas.itemconfig(self.id_loc_shadow, text=data["location"])
        self.canvas.itemconfig(self.id_name, text=data["name"])
        self.canvas.itemconfig(self.id_loc, text=data["location"])
        
        custom_font_size = data.get("font_size")
        if custom_font_size:
            font_size = int(custom_font_size * GLOBAL_SCALE)
        else:
            font_size = self.default_font_size
        
        self.desc_canvas.itemconfig(self.desc_text_id, font=(self.app_font, font_size))
        
        self.scroll_pct = 0.0
        self.desc_canvas.itemconfig(self.desc_text_id, text=data["desc"])
        self.desc_canvas.coords(self.desc_text_id, 5, 5)
        
        self.desc_canvas.update_idletasks()
        bbox = self.desc_canvas.bbox(self.desc_text_id)
        
        if data.get("no_scroll", False):
            self.is_scrollable = False
        else:
            text_h = bbox[3] - bbox[1] if bbox else 0
            self.is_scrollable = (text_h + 20) > self.desc_canvas.winfo_height()
        
        state = 'normal' if self.is_scrollable else 'hidden'
        for i in [self.id_track, self.id_fill, self.id_sb_up, self.id_sb_down, self.sb_handle]:
            self.canvas.itemconfig(i, state=state)
        
        self.update_view()
        self.update_theme(data.get("hex", "#ffffff"))

        aset = self.arrow_cache.get(data.get("arrow", "arrow1.png"), self.arrow_cache.get("arrow1.png"))
        self.current_arrow_set = aset
        if aset:
            self.canvas.itemconfig(self.id_sb_up, image=aset["sb_up"])
            self.canvas.itemconfig(self.id_sb_down, image=aset["sb_down"])
            self.canvas.itemconfig(self.id_btn_prev_shadow, image=aset["left_shadow"])
            self.canvas.itemconfig(self.id_btn_next_shadow, image=aset["right_shadow"])
            self.canvas.itemconfig(self.id_btn_prev, image=aset["left"])
            self.canvas.itemconfig(self.id_btn_next, image=aset["right"])

        folder = data["folder"]
        try:
            bg_path = os.path.join(folder, data["bg"])
            if not os.path.exists(bg_path): bg_path = os.path.join("Niko", "BACKGROUND.png")
            bg_img = Image.open(bg_path).resize((self.win_w, self.win_h), RESAMPLE_MODE)
            self.tk_bg = ImageTk.PhotoImage(bg_img)
            self.canvas.itemconfig(self.id_bg, image=self.tk_bg)

            crop = bg_img.crop((self.bx, self.by, self.bx+self.box_w, self.by+self.box_h))
            dark_layer = Image.new("RGBA", crop.size, (0, 0, 0, BOX_OPACITY)) 
            glass_bg = Image.alpha_composite(crop.convert("RGBA"), dark_layer)
            self.tk_glass_bg = ImageTk.PhotoImage(glass_bg)
            self.canvas.itemconfig(self.id_glass, image=self.tk_glass_bg)

            text_bg_crop = glass_bg.crop((0, 0, self.box_w - s(35), self.box_h))
            self.tk_text_bg = ImageTk.PhotoImage(text_bg_crop)
            self.desc_canvas.itemconfig(self.id_text_bg, image=self.tk_text_bg)
        except: pass

        try:
            p_path = os.path.join(folder, data["portrait"])
            p_img = Image.open(p_path).resize((s(50), s(50)), RESAMPLE_MODE)
            self.portrait_ref = ImageTk.PhotoImage(p_img)
            self.canvas.itemconfig(self.id_portrait, image=self.portrait_ref)
        except: pass

        self.load_sprite_row([os.path.join(folder, spr) for spr in data["sprites"]], data.get("scale_mod", 1.0), data.get("y_offset", 0), data.get("center_single", True), data.get("x_offset", 0))
        
        for tid in [self.id_name_shadow, self.id_name, self.id_track, self.id_fill, self.id_sb_up, self.id_sb_down, self.sb_handle, self.id_btn_prev_shadow, self.id_btn_prev, self.id_btn_next_shadow, self.id_btn_next]:
            self.canvas.tag_raise(tid)

    def load_sprite_row(self, file_paths, scale_mod=1.0, y_offset=0, center_single=True, x_offset=0):
        if self.anim_id: self.root.after_cancel(self.anim_id)
        self.active_gifs = [] 
        for old_id in self.sprite_ids: self.canvas.delete(old_id)
        self.sprite_ids = []

        spacing = int(35 * GLOBAL_SCALE * SPRITE_TWEAK) + 35
        start_x, y_pos = s(80) + s(x_offset), (self.win_h - s(25)) + s(y_offset) 

        idx = 0
        for gif_file in file_paths:
            try:
                if not os.path.exists(gif_file): continue
                img = Image.open(gif_file)
                frames = []
                new_w, new_h = int(img.size[0] * GLOBAL_SCALE * SPRITE_TWEAK * scale_mod), int(img.size[1] * GLOBAL_SCALE * SPRITE_TWEAK * scale_mod)

                if getattr(img, "is_animated", False):
                    for frame in ImageSequence.Iterator(img):
                        frames.append(ImageTk.PhotoImage(frame.copy().resize((new_w, new_h), RESAMPLE_MODE)))
                else:
                    frames.append(ImageTk.PhotoImage(img.copy().resize((new_w, new_h), RESAMPLE_MODE)))

                x = start_x + (1.5 * spacing) if (len(file_paths) == 1 and center_single) else start_x + (idx * spacing)
                sid = self.canvas.create_image(x, y_pos, image=frames[0], anchor="center")
                self.sprite_ids.append(sid)
                self.active_gifs.append({"id": sid, "frames": frames, "current_frame": 0})
                idx += 1
            except: pass
        if self.active_gifs: self.animate_sprites()

    def animate_sprites(self):
        for sprite in self.active_gifs:
            if len(sprite["frames"]) <= 1: continue
            sprite["current_frame"] = (sprite["current_frame"] + 1) % len(sprite["frames"])
            self.canvas.itemconfig(sprite["id"], image=sprite["frames"][sprite["current_frame"]])
        self.anim_id = self.root.after(ANIMATION_SPEED, self.animate_sprites)

    def update_view(self):
        new_y = self.sb_data["top"] + (self.scroll_pct * self.sb_data["len"])
        cx, r = self.sb_data["x"], self.sb_data["r"]
        self.canvas.coords(self.sb_handle, cx, new_y - r, cx + r, new_y, cx, new_y + r, cx - r, new_y)
        self.canvas.coords(self.id_fill, cx - 2, self.sb_data["vis_top"], cx + 2, new_y)
        self.canvas.tag_lower(self.id_fill, self.sb_handle)

        if self.is_scrollable:
            bbox = self.desc_canvas.bbox(self.desc_text_id)
            needed = (bbox[3] - bbox[1]) - self.desc_canvas.winfo_height() if bbox else 0
            self.desc_canvas.coords(self.desc_text_id, 5, 5 - (self.scroll_pct * max(needed + 20, 40)))
        else:
            self.desc_canvas.coords(self.desc_text_id, 5, 5)

    def on_mousewheel(self, event):
        if not self.is_scrollable: return
        bbox = self.desc_canvas.bbox(self.desc_text_id)
        needed = (bbox[3] - bbox[1]) - self.desc_canvas.winfo_height() if bbox else 0
        step = SCROLL_PX_STEP / max(needed + 20, 40)
        self.scroll_pct = max(0, min(1, self.scroll_pct + (step if (event.num == 5 or event.delta < 0) else -step)))
        self.update_view()

    def on_handle_drag(self, event):
        self.scroll_pct = max(0, min(1, (event.y - self.sb_data["top"]) / self.sb_data["len"] if self.sb_data["len"] > 0 else 0))
        self.update_view()

    def next_friend(self):
        self.current_index = (self.current_index + 1) % len(self.friends)
        self.load_friend(self.current_index)

    def prev_friend(self):
        self.current_index = (self.current_index - 1) % len(self.friends)
        self.load_friend(self.current_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = FriendsApp(root)
    root.mainloop()
