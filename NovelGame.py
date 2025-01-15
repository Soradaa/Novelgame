import pyxel

class SceneManager:
    def __init__(self):
        self.scenes = {
            "scene1": {
                "text": [
                    "Scene 1: Repeated Morning",
                    "She: Morning...Another day begins.",
                    "(Light filtering in through the gaps in the curtains illuminates the messy room.)",
                    "She: I have to get up. But there's no reason to get up anymore.",
                    "You: 'Look, it's morning.'",
                    "She:..."
                ],
                "choices": {
                    "Choice 1: 'Are you planning to sleep forever?'": "scene1_choice1",
                    "Choice 2: 'You don't have to push yourself, just do it little by little.'": "scene1_choice2"
                }
            },
            "scene1_choice1": {
                "text": [
                    "She: ...I know. But I can't move.",
                    "You: 'I see. In that case, just letting it rot is also an option.'"
                ],
                "choices": {"Next": "scene2"}
            },
            "scene1_choice2": {
                "text": [
                    "She: Little by little, huh...Yeah, I'll try.",
                    "You: 'That's fine. Let's proceed at your own pace.'"
                ],
                "choices": {"Next": "scene2"}
            },
            "scene2": {
                "text": [
                    "Scene 2: Deserted Cram School",
                    "(An impersonal cram school classroom.",
                    "She sits alone among the neatly arranged desks and chairs.)",
                    "She: It's cold here. Maybe because there's no one here,",
                    "it's chilling to the core.",
                    "You: '...It's cold. But this is your battlefield, right?'"
                ],
                "choices": {
                    "1: 'If you don't like the cold, why don't you leave here?'": "scene2_choice1",
                    "2: 'But you're strong enough here.'": "scene2_choice2"
                }
            },
            "scene2_choice1": {
                "text": [
                    "She: ...I want to leave. But I can't go anywhere.",
                    "You: 'Well, I guess I'll just have to rot away here.'"
                ],
                "choices": {"Next": "scene3"}
            },
            "scene2_choice2": {
                "text": [
                    "She: Strong... me? I've never thought that way.",
                    "You: 'At least, I think you're great for being here.'"
                ],
                "choices": {"Next": "scene3"}
            },
            "scene3": {
                "text": [
                    "Scene 3: A crumbling night",
                    "(A room at midnight. She lies face down on the desk.)",
                    "She: I can't take it anymore. I want to throw it all away.",
                    "I don't want to think about anything.",
                    "You: 'But you're the one who doesn't stop, right?'"
                ],
                "choices": {
                    "1: 'Why don't you just give up? It'll all be for nothing, though.'": "bad_end",
                    "2: 'Let's take a break. But you can still start walking again.'": "scene4"
                }
            },
            "bad_end": {
                "text": [
                    "She: It might be useless... but I don't care anymore.",
                    "You: 'Then it's all over now.'",
                    "Bad End: 'The end of nothingness'"
                ],
                "choices": {}
            },
            "scene4": {
                "text": [
                    "Scene 4: Signs of morning",
                    "(A room with dim light. A workbook spread out on the desk.",
                    "She's made a little more progress than yesterday.)",
                    "She: ...I've made a little more progress than yesterday.",
                    "You: 'That little bit is important.'",
                    "She: ...Thank you.",
                    "You: 'No need to thank me. I'll just keep moving forward with you.'",
                    "Clear End: 'The path to light'"
                ],
                "choices": {}
            }
        }
        self.current_scene = "scene1"
        self.current_text_index = 0

    def get_scene_data(self):
        return self.scenes[self.current_scene]

    def advance_text(self):
        scene = self.get_scene_data()
        if self.current_text_index < len(scene["text"]) - 1:
            self.current_text_index += 1
        else:
            return True  # Indicates all text has been shown
        return False

    def select_choice(self, choice_index):
        scene = self.get_scene_data()
        if "choices" in scene and choice_index < len(scene["choices"]):
            next_scene = list(scene["choices"].values())[choice_index]
            self.current_scene = next_scene
            self.current_text_index = 0


class TextRenderer:
    def __init__(self, manager):
        self.manager = manager

    def draw(self):
        pyxel.cls(0)
        scene = self.manager.get_scene_data()
        y = 10
        for i in range(self.manager.current_text_index + 1):
            pyxel.text(10, y, scene["text"][i], 7)
            y += 10

        if self.manager.current_text_index == len(scene["text"]) - 1 and "choices" in scene:
            y += 10
            for i, (choice_text, _) in enumerate(scene["choices"].items()):
                pyxel.text(10, y + i * 10, f"{choice_text}", 10)


class NovelGame:
    def __init__(self):
        pyxel.init(512, 256, title="Novel Game", fps=30)
        pyxel.mouse(True)  # マウスを有効化
        self.scene_manager = SceneManager()
        self.renderer = TextRenderer(self.scene_manager)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            scene = self.scene_manager.get_scene_data()
            if self.scene_manager.advance_text():
                if "choices" in scene:
                    choice_height = 10 * len(scene["choices"])
                    if 20 <= y <= 20 + choice_height:
                        choice_index = (y - 20) // 10
                        self.scene_manager.select_choice(choice_index)
        elif pyxel.btnp(pyxel.KEY_1):
            self.scene_manager.select_choice(0)
        elif pyxel.btnp(pyxel.KEY_2):
            self.scene_manager.select_choice(1)

    def draw(self):
        self.renderer.draw()


if __name__ == "__main__":
    NovelGame()
