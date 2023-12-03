import streamlit as st
import numpy as np
from PIL import Image
from PIL.Image import fromarray
import noise
import time

# for measuring time
def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))
        return ret
    return wrap

WHT = "#eeeeee"
FONT = ("Tahoma", "15")
FONT2 = ("Tahoma", "8")

class Generator:
    def __init__(self):
        pass

    def get_random_noise(self, scale, shape, octaves, persistence, lacunarity, seed=False):
        scale = shape[1] * (scale / 100)
        persistence /= 100
        lacunarity /= 10
        world = np.zeros(shape)
        if seed == False or seed <= 0:
            seed = np.random.randint(1, 100)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise2(i / scale, j / scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            base=seed)
        return ((world + 1) * 128).astype(np.uint8)

    def assign_colors(self, layers, noise_array, sea_level):
        altitudes = (layers[:, 2] + sea_level).astype(int)
        colors = np.array([np.array([*color], dtype=np.uint8) for color in layers[:, 1]])
        color_indices = np.digitize(noise_array, altitudes)
        color_array = np.array([colors[ind] for ind in color_indices])
        return color_array

    def noise_array_to_image(self, noise_world):
        return fromarray(noise_world, mode="L")

    def color_array_to_image(self, color_world):
        return fromarray(color_world, mode="RGB")


class App:
    def __init__(self, stg, layers):
        self.stg = stg
        self.layers = layers
        self.gen = Generator()
        self.show = True
        self.image = None

    def get_inputs(self):
        for key in self.stg:
            value = int(self.stg[key][0])
            if value < self.stg[key][1]:
                value = self.stg[key][1]  # min
            elif value > self.stg[key][2]:
                value = self.stg[key][2]  # min
            self.stg[key][0] = value

    def default_settings(self):
        for key in self.stg:
            self.stg[key][0] = self.stg[key][1]

    @timing
    def generate(self):
        self.get_inputs()

        noise_array = self.gen.get_random_noise(
            self.stg["scale"][0], (self.stg["height"][0], self.stg["width"][0]), self.stg["octaves"][0],
            self.stg["persistence"][0], self.stg["lacunarity"][0],
            seed=self.stg["seed"][0]
        )
        color_array = self.gen.assign_colors(self.layers, noise_array, self.stg["sea_level"][0])

        self.image = self.gen.color_array_to_image(color_array)

    def draw(self):
        st.image(np.array(self.image), use_column_width=True)
        st.button("Generate", self.generate)

        for key in self.stg:
            self.stg[key][0] = st.sidebar.slider(key, self.stg[key][1], self.stg[key][2], self.stg[key][0], 1)

        st.sidebar.button("Reset to Default", self.default_settings)

        if st.button("Download Image"):
            st.download_button(
                label="Download Image",
                data=Image.fromarray(np.array(self.image)),
                file_name="terrain_image.png",
                key="download_button"
            )

# (default, min, max)
stg = {
    "height": [500, 100, 1000],  # resolution
    "width": [500, 100, 1000],  # resolution
    "seed": [0, 0, 100],  # 0 is random
    "sea_level": [120, 1, 200],  # altitude
    "scale": [45, 1, 100],
    "octaves": [6, 1, 15],
    "persistence": [55, 1, 100],
    "lacunarity": [20, 1, 100]
}

# name, color, altitude
layers = np.array([
    ["blue1", (22, 156, 233), -10],
    ["blue2", (45, 166, 235), -5],
    ["blue3", (68, 176, 238), 0],
    ["beach", (244, 218, 138), 3],
    ["green0", (181, 202, 116), 6],
    ["green1", (116, 186, 94), 25],
    ["green2", (80, 143, 61), 35],
    ["green3", (50, 89, 38), 42],
    ["grey1", (58, 29, 19), 46],
    ["grey2", (92, 61, 61), 52],
    ["snow", (245, 240, 240), 255]
])

st.set_page_config(layout="wide")
st.title("MapGen🏞️")

# Use st.session_state to persistently store the state across sessions
if "state" not in st.session_state:
    st.session_state.state = stg.copy()

app = App(st.session_state.state, layers)
app.generate()
app.draw()
