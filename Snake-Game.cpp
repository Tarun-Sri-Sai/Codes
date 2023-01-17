#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <windows.h>
#include <conio.h>

using namespace std;

const int WIDTH = 40, HEIGHT = 20, ESC = 27, LOOP_TIMER = 100, MAX_SCORE = (WIDTH * HEIGHT) / 4;

bool game_over = false;
int head_x, head_y, fruit_x, fruit_y, score;
int next_direction[][2] = {
    {0, 0},  //  STOP
    {1, 0},  //  RIGHT
    {0, -1}, //  UP
    {-1, 0}, //  LEFT
    {0, 1}   //  DOWN
};

enum e_direction
{
    STOP = 0,
    RIGHT,
    UP,
    LEFT,
    DOWN
} direction;

enum e_mode {
    FREEPLAY = 0,
    CAMPAIGN
} mode;

void setup();
void draw();
void input();
void logic();
int bounded_rand(int lb, int ub);
void freeplay();
void update_score();
void update_directions();
bool is_side_border(int j);
bool is_head(int i, int j);
bool is_fruit(int i, int j);
void generate_fruit();
void take_directions();

/**
 *
 * DRIVER FUNCTION
 *
 */
int main()
{
    srand(time(NULL));
    setup();
    draw();
    while (!game_over && score < MAX_SCORE)
    {
        clock_t start_time = clock();
        input();
        logic();
        draw();
        clock_t time_taken = clock() - start_time;
        if (time_taken < LOOP_TIMER)
        {
            Sleep(LOOP_TIMER - time_taken);
        }
    }
    if (score >= MAX_SCORE)
    {
        printf("\nDamn you really beat the Snake Game! :D\n");
    }
    return 0;
}

void setup()
{
    game_over = false;
    head_x = 1 + WIDTH / 2;
    head_y = 1 + HEIGHT / 2;
    generate_fruit();
    direction = STOP;
    system("cls");
}

void draw()
{
    /**
     * Replacement for:
     * system("cls");
    */
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), {0,0}); 
    for (int i = 0; i < HEIGHT + 2; ++i)
    {
        if (i == 0 || i == HEIGHT + 1)
        {
            for (int i = 0; i < WIDTH + 2; ++i)
            {
                cout << '#';
            }
            cout << '\n';
            continue;
        }
        for (int j = 0; j < WIDTH + 2; ++j)
        {
            if (is_side_border(j))
            {
                cout << '#';
            }
            else if (is_head(i, j))
            {
                cout << 'O';
            }
            else if (is_fruit(i, j))
            {
                cout << '@';
            }
            else
            {
                cout << ' ';
            }
        }
        cout << '\n';
    }
    cout << "Score: " << score << '\n';
}

bool is_fruit(int i, int j)
{
    return j == fruit_x && i == fruit_y;
}

bool is_head(int i, int j)
{
    return j == head_x && i == head_y;
}

bool is_side_border(int j)
{
    return j == 0 || j == WIDTH + 1;
}

int bounded_rand(int lb, int ub)
{
    return lb + rand() % (ub - lb + 1);
}

void input()
{
    if (_kbhit())
    {
        take_directions();
    }
}

void take_directions()
{
    switch (getch())
    {
    case 'a':
        direction = LEFT;
        break;
    case 'w':
        direction = UP;
        break;
    case 's':
        direction = DOWN;
        break;
    case 'd':
        direction = RIGHT;
        break;
    case ESC:
        direction = STOP;
        game_over = true;
        break;
    }
}

void logic()
{
    update_directions();
    freeplay();
    update_score();
}

void update_directions() {
    head_x += next_direction[direction][0];
    head_y += next_direction[direction][1];
}

void freeplay()
{
    if (head_x == 0)
    {
        head_x = WIDTH;
    }
    if (head_x == WIDTH + 1)
    {
        head_x = 1;
    }
    if (head_y == 0)
    {
        head_y = HEIGHT;
    }
    if (head_y == HEIGHT + 1)
    {
        head_y = 1;
    }
}

void update_score()
{
    if (is_fruit(head_x, head_y))
    {
        ++score;
        fruit_x = bounded_rand(1, WIDTH);
        fruit_y = bounded_rand(1, HEIGHT);
    }
}

void generate_fruit()
{
    fruit_x = bounded_rand(1, WIDTH);
    fruit_y = bounded_rand(1, HEIGHT);
}