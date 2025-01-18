#ifndef ANSI_ESCAPES_H
#define ANSI_ESCAPES_H

#include <stdio.h>

enum Colors
{
    RESET_COLOR,
    BLACK_TXT = 30,
    RED_TXT,
    GREEN_TXT,
    YELLOW_TXT,
    BLUE_TXT,
    MAGENTA_TXT,
    CYAN_TXT,
    WHITE_TXT,

    BLACK_BKG = 40,
    RED_BKG,
    GREEN_BKG,
    YELLOW_BKG,
    BLUE_BKG,
    MAGENTA_BKG,
    CYAN_BKG,
    WHITE_BKG
};

enum ClearCodes
{
    CLEAR_FROM_CURSOR_TO_END,
    CLEAR_FROM_CURSOR_TO_BEGIN,
    CLEAR_ALL
};

void setupConsole(void);
void restoreConsole(void);
void getCursorPosition(int *row, int *col);
static inline void setTextColor(int code)
static inline void setTextColorBright(int code)
static inline void setBackgroundColor(int code)
static inline void setBackgroundColorBright(int code)
static inline void resetColor(void)
static inline void clearScreen(void)
static inline void clearScreenToBottom(void)
static inline void clearScreenToTop(void)
static inline void clearLine(void)
static inline void clearLineToRight(void)
static inline void clearLineToLeft(void)
static inline void moveUp(int positions)
static inline void moveDown(int positions)
static inline void moveRight(int positions)
static inline void moveLeft(int positions)
static inline void moveTo(int row, int col)
static inline void saveCursorPosition(void)
static inline void restoreCursorPosition(void)

#endif
