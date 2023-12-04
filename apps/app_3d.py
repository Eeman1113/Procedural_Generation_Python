import streamlit as st
import noise
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

WHT = "#eeeeee"
FONT = ("Tahoma", "15")
FONT2 = ("Tahoma", "8")


class Generator:
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

    


def visualize_3d(noise_array, color_array):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    height, width = noise_array.shape
    x = np.arange(0, width, 1)
    y = np.arange(0, height, 1)

    X, Y = np.meshgrid(x, y)
    Z = noise_array

    # Map colors for the 3D plot based on the color_array
    color_mapping = np.array(color_array).reshape((height, width, 3)) / 255.0

    # Plot the 3D surface with color mapping
    ax.plot_surface(X, Y, Z, facecolors=color_mapping, rstride=1, cstride=1, antialiased=False, shade=False)

    st.pyplot(fig)


def generate_noise_image(scale, shape, octaves, persistence, lacunarity, seed):
    gen = Generator()
    noise_array = gen.get_random_noise(scale, shape, octaves, persistence, lacunarity, seed)
    return noise_array


def generate_color_array(layers, noise_array, sea_level):
    gen = Generator()
    color_array = gen.assign_colors(layers, noise_array, sea_level)
    return color_array


# Define layers outside the functions
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


def main():
    st.title("Terrain Generator")

    st.sidebar.header("Settings")

    scale = st.sidebar.slider("Scale", 1, 100, 45)
    octaves = st.sidebar.slider("Octaves", 1, 15, 6)
    persistence = st.sidebar.slider("Persistence", 1, 100, 55)
    lacunarity = st.sidebar.slider("Lacunarity", 1, 100, 20)
    seed = st.sidebar.slider("Seed", 0, 100, 0)
    sea_level = st.sidebar.slider("Sea Level", 1, 200, 120)

    generate_button = st.sidebar.button("Generate")
    if generate_button:
        shape = (st.sidebar.slider("Height", 10, 1000, 500), st.sidebar.slider("Width", 10, 2000, 1000))
        noise_array = generate_noise_image(scale, shape, octaves, persistence, lacunarity, seed)
        color_array = generate_color_array(layers, noise_array, sea_level)

        # Display the generated image
        st.image(color_array, use_column_width=True, channels='RGB')

        # Visualize in 3D
        visualize_3d(noise_array, color_array)


if __name__ == "__main__":
    main()
