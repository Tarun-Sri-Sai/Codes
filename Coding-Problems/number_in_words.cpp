#include <bits/stdc++.h>
using namespace std;

#define long long long

unordered_map<int, string> inWords;

void mapInit();
string numToStr(long num);
vector<string> threeDigitToStr(vector<int> threeDigits);
string twoDigitToStr(int tensPlace, int onesPlace);

int main()
{
    mapInit();
    long num;
    cin >> num;
    cout << numToStr(num) << '\n';
    return 0;
}

void mapInit()
{
    inWords = {{0, "Zero"},
               {1, "One"},
               {2, "Two"},
               {3, "Three"},
               {4, "Four"},
               {5, "Five"},
               {6, "Six"},
               {7, "Seven"},
               {8, "Eight"},
               {9, "Nine"},
               {10, "Ten"},
               {11, "Eleven"},
               {12, "Twelve"},
               {13, "Thirteen"},
               {14, "Fourteen"},
               {15, "Fifteen"},
               {16, "Sixteen"},
               {17, "Seventeen"},
               {18, "Eighteen"},
               {19, "Nineteen"},
               {20, "Twenty"},
               {30, "Thirty"},
               {40, "Forty"},
               {50, "Fifty"},
               {60, "Sixty"},
               {70, "Seventy"},
               {80, "Eighty"},
               {90, "Ninety"}
              };
}

string numToStr(long num)
{
    if (num == 0)
    {
        return "Zero";
    }
    string result = "";
    vector<int> threeDigits;
    while (num > 0)
    {
        threeDigits.push_back((int)(num % 1000LL));
        num /= 1000LL;
    }
    vector<string> threeDigitStrings = threeDigitToStr(threeDigits);
    int size = threeDigitStrings.size();
    vector<string> placeValue = {"",
                              "Thousand",
                              "Million",
                              "Billion",
                              "Trillion",
                              "Quadrillion",
                              "Quintillion",
                              "Sextillion"
                             };
    vector<string> resultGroup;
    for (int i = 0; i < size; i++)
    {
        if (threeDigitStrings[i].compare("Zero") == 0)
        {
            continue;
        }
        resultGroup.push_back(placeValue[i]);
        resultGroup.push_back(threeDigitStrings[i]);
    }
    reverse(resultGroup.begin(), resultGroup.end());
    for (int i = 0, groupSize = resultGroup.size(); i < groupSize; i++)
    {
        result += resultGroup[i];
        if (i == groupSize - 1)
        {
            break;
        }
        result += " ";
    }
    result.erase(result.find_last_not_of(" \n\r\t")+1);
    return result;
}

vector<string> threeDigitToStr(vector<int> threeDigits)
{
    vector<string> result;
    for (int threeDigit : threeDigits)
    {
        string threeDigitStr;
        int onesPlace = threeDigit % 10;
        int tensPlace = (threeDigit / 10) % 10;
        int hunsPlace = (threeDigit / 100) % 10;
        string twoDigitStr = twoDigitToStr(tensPlace, onesPlace);
        if (hunsPlace == 0) {
            result.push_back(twoDigitStr);
            continue;
        }
        result.push_back(inWords[hunsPlace] + " Hundred" 
                         + (twoDigitStr.compare("Zero") == 0 ?
                             "" : 
                             " and " + twoDigitStr));
    }
    return result;
}

string twoDigitToStr(int tensPlace, int onesPlace)
{
    if (tensPlace <= 1 || onesPlace == 0)
    {
        return inWords[tensPlace * 10 + onesPlace];
    }
    return inWords[tensPlace * 10] + (" " + inWords[onesPlace]);
}