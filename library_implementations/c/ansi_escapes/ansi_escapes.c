#include "ansi_escapes.h"

static inline void setTextColor(int code)
{
    printf("\x1b[%dm", code);
}

static inline void setTextColorBright(int code)
{
    printf("\x1b[%d;1m", code);
}

static inline void setBackgroundColor(int code)
{
    printf("\x1b[%dm", code);
}

static inline void setBackgroundColorBright(int code)
{
    printf("\x1b[%d;1m", code);
}

static inline void resetColor(void)
{
    printf("\x1b[%dm", RESET_COLOR);
}

static inline void clearScreen(void)
{
    printf("\x1b[%dJ", CLEAR_ALL);
}

static inline void clearScreenToBottom(void)
{
    printf("\x1b[%dJ", CLEAR_FROM_CURSOR_TO_END);
}

static inline void clearScreenToTop(void)
{
    printf("\x1b[%dJ", CLEAR_FROM_CURSOR_TO_BEGIN);
}

static inline void clearLine(void)
{
    printf("\x1b[%dK", CLEAR_ALL);
}

static inline void clearLineToRight(void)
{
    printf("\x1b[%dK", CLEAR_FROM_CURSOR_TO_END);
}

static inline void clearLineToLeft(void)
{
    printf("\x1b[%dK", CLEAR_FROM_CURSOR_TO_BEGIN);
}

static inline void moveUp(int positions)
{
    printf("\x1b[%dA", positions);
}

static inline void moveDown(int positions)
{
    printf("\x1b[%dB", positions);
}

static inline void moveRight(int positions)
{
    printf("\x1b[%dC", positions);
}

static inline void moveLeft(int positions)
{
    printf("\x1b[%dD", positions);
}

static inline void moveTo(int row, int col)
{
    printf("\x1b[%d;%df", row, col);
}

static inline void saveCursorPosition(void)
{
    printf("\x1b%d", 7);
}

static inline void restoreCursorPosition(void)
{
    printf("\x1b%d", 8);
}
