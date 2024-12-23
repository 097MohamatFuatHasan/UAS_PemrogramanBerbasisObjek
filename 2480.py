import pygame
import random
import sys

# CONSTANTS
SCREEN_SIZE = 400  # Ukuran layar game, 400px x 400px
GRID_SIZE = 4  # Ukuran grid 4x4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE  # Ukuran setiap tile, dibagi ukuran layar dengan ukuran grid
BACKGROUND_COLOR = (187, 173, 160)  # Warna latar belakang grid
TILE_COLORS = {  # Warna untuk setiap nilai tile
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Base Tile Class (Parent Class)
class Tile:
    def __init__(self, value, position):
        self.value = value  # Nilai dari tile (misalnya 2, 4, 8, dst)
        self.position = position  # Posisi tile di grid (baris, kolom)

    def merge(self, other):
        # Metode untuk menggabungkan dua tile jika nilainya sama
        if self.value == other.value:
            self.value *= 2  # Menggandakan nilai tile
            return True
        return False

    def render(self, screen, x, y):
        # Menggambar tile di layar
        rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Membuat rect untuk tile
        color = TILE_COLORS.get(self.value, (205, 193, 180))  # Memilih warna berdasarkan nilai
        pygame.draw.rect(screen, color, rect, border_radius=5)  # Menggambar persegi panjang untuk tile
        font = pygame.font.Font(None, 72)  # Font untuk nilai tile
        text = font.render(str(self.value), True, (119, 110, 101))  # Menampilkan nilai tile
        text_rect = text.get_rect(center=rect.center)  # Menempatkan teks di tengah tile
        screen.blit(text, text_rect)  # Menampilkan teks pada layar

# PowerTile Class (Subclass of Tile)
class PowerTile(Tile):
    def __init__(self, value, position, power):
        super().__init__(value, position)  # Memanggil konstruktor kelas induk (Tile)
        self.power = power  # Kekhususan: Power untuk tile (misalnya, kekuatan tambahan saat menggabung)

    def merge(self, other):
        # Polimorfisme: Menggabungkan tile dengan kekuatan tambahan
        if self.value == other.value:
            self.value *= 2  # Menggandakan nilai tile
            self.power += 1  # Meningkatkan kekuatan tile setelah penggabungan
            return True
        return False

    def render(self, screen, x, y):
        super().render(screen, x, y)  # Menggunakan render dari kelas induk (Tile)
        # Menampilkan power atau detail khusus lainnya pada tile
        font = pygame.font.Font(None, 32)
        power_text = font.render(f"Power: {self.power}", True, (0, 0, 0))  # Menampilkan teks power
        text_rect = power_text.get_rect(center=(y * TILE_SIZE + TILE_SIZE // 2, x * TILE_SIZE + TILE_SIZE // 2 + 40))
        screen.blit(power_text, text_rect)  # Menampilkan power di layar

# Grid Class
class Grid:
    def __init__(self, size):
        self.size = size  # Ukuran grid (4x4)
        self.tiles = [[None for _ in range(size)] for _ in range(size)]  # Matriks kosong untuk grid
        self.add_tile()  # Menambahkan tile pertama
        self.add_tile()  # Menambahkan tile kedua

    def add_tile(self):
        # Menambahkan tile baru ke grid pada posisi kosong secara acak
        empty_positions = [
            (x, y) for x in range(self.size) for y in range(self.size) 
            if self.tiles[x][y] is None
        ]
        if empty_positions:
            x, y = random.choice(empty_positions)  # Memilih posisi kosong secara acak
            tile_type = random.choice([Tile, PowerTile])  # Secara acak memilih tile biasa atau PowerTile
            if tile_type == PowerTile:
                power = random.randint(1, 5)  # Memberikan nilai power acak antara 1 dan 5
                self.tiles[x][y] = tile_type(random.choice([2, 4]), (x, y), power)  # Membuat PowerTile
            else:
                self.tiles[x][y] = tile_type(random.choice([2, 4]), (x, y))  # Membuat Tile biasa

    def slide(self, direction):
        # Menggeser grid sesuai arah yang diberikan
        if direction == "up":
            self.tiles = self.rotate_left(self.tiles)  # Rotasi grid ke kiri untuk memudahkan pergeseran
            moved = self._slide_left()  # Geser grid ke kiri
            self.tiles = self.rotate_right(self.tiles)  # Kembalikan rotasi ke kanan
        elif direction == "down":
            self.tiles = self.rotate_right(self.tiles)  # Rotasi grid ke kanan
            moved = self._slide_left()  # Geser grid ke kiri
            self.tiles = self.rotate_left(self.tiles)  # Kembalikan rotasi ke kiri
        elif direction == "left":
            moved = self._slide_left()  # Geser grid ke kiri
        elif direction == "right":
            self.tiles = self.reverse(self.tiles)  # Membalikkan grid secara horizontal
            moved = self._slide_left()  # Geser grid ke kiri
            self.tiles = self.reverse(self.tiles)  # Kembalikan grid seperti semula
        else:
            return False

        if moved:
            self.add_tile()  # Menambahkan tile baru setelah pergeseran
        return moved

    def _slide_left(self):
        # Fungsi untuk menggeser semua baris ke kiri, dan menggabungkan nilai yang sama
        moved = False
        for row in self.tiles:
            new_row = [tile for tile in row if tile]  # Hapus None dari baris
            merged_row = []
            skip = False
            for i in range(len(new_row)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(new_row) and new_row[i].value == new_row[i + 1].value:
                    if new_row[i].merge(new_row[i + 1]):  # Menggabungkan tile yang memiliki nilai sama
                        merged_row.append(new_row[i])
                        skip = True
                else:
                    merged_row.append(new_row[i])
            merged_row += [None] * (self.size - len(merged_row))  # Mengisi sisa baris dengan None
            if [tile.value if tile else None for tile in row] != [tile.value if tile else None for tile in merged_row]:
                moved = True
            for i in range(self.size):
                row[i] = merged_row[i]
        return moved

    def rotate_left(self, tiles):
        return [list(row) for row in zip(*tiles)][::-1]  # Rotasi grid ke kiri

    def rotate_right(self, tiles):
        return [list(row) for row in zip(*tiles[::-1])]  # Rotasi grid ke kanan

    def reverse(self, tiles):
        return [row[::-1] for row in tiles]  # Membalikkan grid secara horizontal

    def is_game_over(self):
        # Mengecek apakah permainan sudah selesai
        for x in range(self.size):
            for y in range(self.size):
                if self.tiles[x][y] is None:
                    return False  # Masih ada tile kosong
                if y < self.size - 1 and self.tiles[x][y] is not None and self.tiles[x][y + 1] is not None:
                    if self.tiles[x][y].value == self.tiles[x][y + 1].value:
                        return False  # Ada tile yang bisa digabungkan secara horizontal
                if x < self.size - 1 and self.tiles[x][y] is not None and self.tiles[x + 1][y] is not None:
                    if self.tiles[x][y].value == self.tiles[x + 1][y].value:
                        return False  # Ada tile yang bisa digabungkan secara vertikal
        return True

# Renderer Class
class Renderer:
    def __init__(self, screen):
        self.screen = screen  # Layar tempat game ditampilkan

    def render(self, grid):
        self.screen.fill(BACKGROUND_COLOR)  # Mengisi latar belakang dengan warna
        for x in range(grid.size):
            for y in range(grid.size):
                tile = grid.tiles[x][y]
                if tile:
                    tile.render(self.screen, x, y)  # Menggambar setiap tile di grid

# GameManager Class
class GameManager:
    def __init__(self):
        pygame.init()  # Inisialisasi pygame
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))  # Membuat layar game
        pygame.display.set_caption("2048")  # Menetapkan judul window
        self.grid = Grid(GRID_SIZE)  # Membuat grid permainan
        self.renderer = Renderer(self.screen)  # Membuat renderer untuk menggambar ke layar
        self.running = True  # Status permainan (apakah masih berjalan)

    def run(self):
        clock = pygame.time.Clock()  # Menetapkan kecepatan permainan
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Keluar dari permainan

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.grid.slide("up")  # Geser grid ke atas
                    elif event.key == pygame.K_DOWN:
                        self.grid.slide("down")  # Geser grid ke bawah
                    elif event.key == pygame.K_LEFT:
                        self.grid.slide("left")  # Geser grid ke kiri
                    elif event.key == pygame.K_RIGHT:
                        self.grid.slide("right")  # Geser grid ke kanan
            
            self.renderer.render(self.grid)  # Gambar grid ke layar
            pygame.display.flip()  # Update layar
            clock.tick(60)  # Menjaga agar permainan berjalan pada 60 FPS
            
            if self.grid.is_game_over():
                self.running = False  # Jika permainan berakhir, keluar dari loop
                self.display_game_over()

        pygame.quit()  # Menutup pygame
        sys.exit()  # Keluar dari program

    def display_game_over(self):
        # Menampilkan layar Game Over
        self.screen.fill(BACKGROUND_COLOR)  # Mengisi layar dengan warna latar belakang
        font = pygame.font.Font(None, 72)  # Font untuk teks Game Over
        text = font.render("Game Over", True, (255, 0, 0))  # Menampilkan teks Game Over
        text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))  # Menempatkan teks di tengah layar
        self.screen.blit(text, text_rect)  # Menampilkan teks
        pygame.display.flip()  # Update layar
        pygame.time.wait(3000)  # Tunggu 3 detik sebelum keluar

if __name__ == "__main__":
    game = GameManager()  # Membuat objek GameManager
    game.run()  # Menjalankan permainan
