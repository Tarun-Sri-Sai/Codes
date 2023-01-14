#include <iostream>
#include <vector>
#include <string>
#define long long long
using namespace std;

class Rsa
{
private:
    int p, q, n, m, e, d;

    int gcd(int a, int b)
    {
        if (a == 0)
            return b;
        if (b == 0)
            return a;
        if (a == b)
            return a;
        if (a < b)
            return gcd(a, b - a);
        return gcd(a - b, a);
    }

    int public_key(int m)
    {
        for (int i = 2; i < m; i++)
            if (gcd(i, m) == 1)
                return i;
        return 0;
    }

    int private_key(int e, int m)
    {
        for (int i = 2; i < m; i++)
            if ((e * i) % m == 1)
                return i;
        return 0;
    }

    int power_mod(int base, int exp, int mod)
    {
        int x = base, ans = 1;
        while (exp > 0)
        {
            if (exp % 2 != 0)
                ans = (ans * x) % mod;
            x = (x * x) % mod;
            exp /= 2;
        }
        return ans;
    }

public:
    Rsa(int p, int q)
    {
        this->p = p;
        this->q = q;
        n = p * q;
        m = (p - 1) * (q - 1);
        e = public_key(m);
        d = private_key(e, m);
    }

    pair<int, int> get_public_key()
    {
        return {n, e};
    }

    int encrypt(int x)
    {
        return power_mod(x, e, n);
    }

    int decrypt(int x)
    {
        return power_mod(x, d, n);
    }
};

int main()
{
    int p = 13, q = 29;
    Rsa rsa(p, q);
    string s = "Mango fruit", cipher_text;
    vector<int> cipher;
    // cout << s << '\n';
    for (int len = s.length(), i = 0; i < len; i++)
    {
        cipher.push_back(rsa.encrypt((int)s[i]));
        cipher_text.push_back((char)(cipher[i] % 256));
    }
    cout << cipher_text << '\n';
    string decipher;
    for (int len = cipher.size(), i = 0; i < len; i++)
        decipher += (char)rsa.decrypt(cipher[i]);
    cout << decipher << '\n';
    return 0;
}