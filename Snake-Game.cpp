#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <windows.h>
#include <conio.h>

using namespace std;

const int WIDTH = 40, HEIGHT = 20, ESC = 27, LOOP_TIMER = 75, MAX_SCORE = (WIDTH * HEIGHT) / 4;

bool game_over;
int head_x, head_y, fruit_x, fruit_y, score;
int tail_x[MAX_SCORE + 1], tail_y[MAX_SCORE + 1];
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
int bounded_rand(int lower_bound, int upper_bound);
void freeplay();
void update_score();
void update_directions();
bool is_side_border(int position_x);
bool is_head(int position_y, int position_x);
bool is_fruit(int position_y, int position_x);
void generate_fruit();
void get_direction_input();
void update_tail();
bool is_tail(int position_y, int position_x);
void debug_print_tail();

/**
 *
 * DRIVER FUNCTION
 *
 */
int main()
{
    srand(time(NULL));
    setup();
    while (!game_over && score < MAX_SCORE)
    {
        draw();
        input();
        logic();
    }
    // debug_print_tail();
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
    printf("\x1b[d");
    for (int position_y = 0; position_y < HEIGHT + 2; ++position_y)
    {
        if (position_y == 0 || position_y == HEIGHT + 1)
        {
            for (int position_y = 0; position_y < WIDTH + 2; ++position_y)
            {
                putchar('#');
            }
            putchar('\n');
            continue;
        }
        for (int position_x = 0; position_x < WIDTH + 2; ++position_x)
        {
            if (is_side_border(position_x))
            {
                putchar('#');
            }
            else if (is_head(position_y, position_x))
            {
                putchar('O');
            }
            else if (is_fruit(position_y, position_x))
            {
                putchar('@');
            }
            else if (is_tail(position_y, position_x))
            {
                putchar('o');
            }
            else
            {
                putchar(' ');
            }
        }
        putchar('\n');
    }
    cout << "Score: " << score << '\n';
}

bool is_fruit(int position_y, int position_x)
{
    return position_x == fruit_x && position_y == fruit_y;
}

bool is_head(int position_y, int position_x)
{
    return position_x == head_x && position_y == head_y;
}

bool is_side_border(int position_x)
{
    return position_x == 0 || position_x == WIDTH + 1;
}

int bounded_rand(int lower_bound, int upper_bound)
{
    return lower_bound + rand() % (upper_bound - lower_bound + 1);
}

void input()
{
    const int LIMIT = (direction == UP || direction == DOWN ? LOOP_TIMER * 100 : LOOP_TIMER * 50);
    int i = 0;
    do {
        if (_kbhit())
        {
            get_direction_input();
        }
    } while (++i < LIMIT);
}

void get_direction_input()
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
    if (is_tail(head_y, head_x))
    {
        game_over = true;
    }
    update_tail();
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
    if (is_fruit(head_y, head_x))
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

void update_tail()
{
    int prev_x = tail_x[0];
    int prev_y = tail_y[0];
    int temp_x, temp_y;
    tail_x[0] = head_x;
    tail_y[0] = head_y;
    for (int i = 1; i < score; ++i)
    {
        temp_x = tail_x[i];
        temp_y = tail_y[i];
        tail_x[i] = prev_x;
        tail_y[i] = prev_y;
        prev_x = temp_x;
        prev_y = temp_y;
    }
}

bool is_tail(int position_y, int position_x)
{
    for (int i = 0; i < score; ++i)
    {
        if (tail_x[i] == position_x && tail_y[i] == position_y)
        {
            return true;
        }
    }
    return false;
}

void debug_print_tail()
{
    for (int i = 0; i < score; ++i)
    {
        cerr << '(' << tail_x[i] << ", " << tail_y[i] << ")\n";
    }
}