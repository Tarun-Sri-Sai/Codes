import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class RSA {
    private PublicKey publicKey;
    private PrivateKey privateKey;
    private Random random;

    public RSA() {
        random = new Random(System.currentTimeMillis());
        Primes primes = new Primes();
        int prime1 = primes.getRandom(), prime2 = primes.getRandom();
        int modulus = prime1 * prime2, totient = (prime1 - 1) * (prime2 - 1);
        KeyExponents keyExponents = getKeyExponents(totient, modulus);
        publicKey = new PublicKey(modulus, keyExponents.publicKeyExponent);
        privateKey = new PrivateKey(modulus, keyExponents.privateKeyExponent);
    }

    public PublicKey getPublicKey() {
        return publicKey;
    }

    public PrivateKey getPrivateKey() {
        return privateKey;
    }

    public KeyExponents getKeyExponents(int totient, int modulus) {
        List<Integer> publicKeyExponents = new ArrayList<>();
        for (int i = 2; i < totient; i++) {
            if (gcd(totient, i) == 1) {
                publicKeyExponents.add(i);
            }
        }
        if (publicKeyExponents.size() == 0) {
            throw new IllegalArgumentException("Public key exponent not found");
        }
        int publicKeyExponent = publicKeyExponents.remove(random.nextInt(publicKeyExponents.size()));
        int privateKeyExponent = 1;
        while (true) {
            try {
                privateKeyExponent = getPrivateKeyExponent(publicKeyExponent, totient);
                break;
            } catch (IllegalArgumentException iae) {
                try {
                    publicKeyExponent = publicKeyExponents.remove(random.nextInt(publicKeyExponents.size()));
                } catch (IllegalArgumentException iae2) {
                    throw new IllegalArgumentException("Public key exponent not found after running err of available keys");
                }
            }
        }
        return new KeyExponents(publicKeyExponent, privateKeyExponent);
    }

    private int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    private int getPrivateKeyExponent(int publicKeyExponent, int totient) {
        List<Integer> results = new ArrayList<>();
        for (int i = 1; i < totient; i++) {
            if (RSA.mul(publicKeyExponent, i, totient) % totient == 1) {
                results.add(i);
            }
        }
        if (results.size() == 0) {
            throw new IllegalArgumentException("Private key exponent not found");
        }
        return results.get(random.nextInt(results.size()));
    }

    private static int mul(int a, int b, int mod) {
        return (int) (((long) a * b) % mod);
    }

    private static int power(int base, int exponent, int modulus) {
        int result = 1, multiplier = base;
        while (exponent != 0) {
            if (exponent % 2 != 0) {
                result = mul(result, multiplier, modulus);
            }
            multiplier = mul(multiplier, multiplier, modulus);
            exponent /= 2;
        }
        return result;
    }

    public class PublicKey {
        private int modulus, publicKeyExponent;

        private PublicKey(int modulus, int publicKeyExponent) {
            this.modulus = modulus;
            this.publicKeyExponent = publicKeyExponent;
        }

        public int[] encrypt(String plainText) {
            int length = plainText.length();
            int[] result = new int[length];
            for (int i = 0; i < length; i++) {
                result[i] = RSA.power((int)plainText.charAt(i), publicKeyExponent, modulus);
            }
            return result;
        }
    }

    public class PrivateKey {
        private int modulus, privateKeyExponent;

        private PrivateKey(int modulus, int privateKeyExponent) {
            this.modulus = modulus;
            this.privateKeyExponent = privateKeyExponent;
        }

        public String decrypt(int[] encryptedText) {
            int length = encryptedText.length;
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < length; i++) {
                result.append((char)((RSA.power(encryptedText[i], privateKeyExponent, modulus) + 128) % 128));
            }
            return result.toString();
        }
    }

    private class KeyExponents {
        public int publicKeyExponent, privateKeyExponent;

        public KeyExponents(int publicKeyExponent, int privateKeyExponent) {
            this.publicKeyExponent = publicKeyExponent;
            this.privateKeyExponent = privateKeyExponent;
        }
    }

    private class Primes {
        private List<Integer> primes;
        private Random random;
        private static final int MAX_PRIME = 99, MIN_PRIME = MAX_PRIME / 10;
    
        public Primes() {
            random = new Random(System.currentTimeMillis());
            primes = new ArrayList<>();
            boolean[] isPrime = new boolean[MAX_PRIME + 1];
            Arrays.fill(isPrime, true);
            isPrime[0] = isPrime[1] = false;
            for (int i = 2; i <= MAX_PRIME; i++) {
                if (!isPrime[i]) {
                    continue;
                }
                primes.add(i);
                for (int j = i * i; j <= MAX_PRIME; j += i) {
                    isPrime[j] = false;
                }
            }
            while (primes.get(0) <= MIN_PRIME) {
                primes.remove(0);
            }
        }
    
        public int getRandom() {
            return primes.remove(random.nextInt(primes.size()));
        }
    }
}