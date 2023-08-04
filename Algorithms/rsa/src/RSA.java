package src;

import java.util.*;

public class RSA {
    private PublicKey publicKey;
    private PrivateKey privateKey;
    private Random random;
    private static final int PUBLIC_KEY_EXPONENT = 65537, MAX_SIZE = 10;

    public RSA() {
        random = new Random(System.currentTimeMillis());
        Primes primes = new Primes(4);
        int prime1 = primes.getRandom(), prime2 = primes.getRandom();
        int modulus = prime1 * prime2, totient = (prime1 - 1) * (prime2 - 1);
        publicKey = new PublicKey(modulus, PUBLIC_KEY_EXPONENT);
        int privateKeyExponent = getPrivateKeyExponent(PUBLIC_KEY_EXPONENT, totient);
        privateKey = new PrivateKey(modulus, privateKeyExponent);
    }

    public PublicKey getPublicKey() {
        return publicKey;
    }

    public PrivateKey getPrivateKey() {
        return privateKey;
    }

    private int getPrivateKeyExponent(int publicKeyExponent, int totient) {
        List<Integer> results = new ArrayList<>();
        for (int i = 1; i < totient; i++) {
            if (RSA.mul(publicKeyExponent, i, totient) % totient == 1) {
                results.add(i);
            }
            if (results.size() > MAX_SIZE) {
                break;
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
                result[i] = RSA.power((int) plainText.charAt(i), publicKeyExponent, modulus);
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
                result.append((char) RSA.power(encryptedText[i], privateKeyExponent, modulus));
            }
            return result.toString();
        }
    }

    private class Primes {
        private List<Integer> primes;
        private Random random;
        private final int MAX_PRIME, MIN_PRIME;

        private Primes(int digits) {
            MAX_PRIME = largestNum(digits);
            MIN_PRIME = MAX_PRIME / 10 + 1;
            random = new Random(System.currentTimeMillis());
            primes = segmentedSeive(MIN_PRIME, MAX_PRIME);
        }

        private int getRandom() {
            int randIndex = random.nextInt(primes.size());
            Integer result = primes.get(randIndex);
            while (result == null) {
                result = primes.get(randIndex);
            }
            primes.set(randIndex, null);
            return result;
        }

        private int largestNum(int digits) {
            int result = 0;
            for (int i = 0; i < digits; i++) {
                result = result * 10 + 9;
            }
            return result;
        }

        private List<Integer> segmentedSeive(int minValue, int maxValue) {
            int maxSqrt = (int) Math.ceil(Math.sqrt(maxValue));
            boolean[] isPrime = seive(maxSqrt);
            boolean[] isPrimeRange = new boolean[maxValue - minValue + 1];
            Arrays.fill(isPrimeRange, true);
            for (int length = isPrime.length, i = 2; i < length; i++) {
                for (int j = ceilMultiple(i, minValue); j <= maxValue; j += i) {
                    isPrimeRange[j - minValue] = false;
                }
            }
            List<Integer> result = new ArrayList<>();
            for (int i = minValue; i <= maxValue; i++) {
                if (isPrimeRange[i - minValue]) {
                    result.add(i);
                }
            }
            return result;
        }

        private boolean[] seive(int maxValue) {
            boolean[] result = new boolean[maxValue + 1];
            Arrays.fill(result, true);
            for (int i = 2; i * i <= maxValue; i++) {
                if (!result[i]) {
                    continue;
                }
                for (int j = i * i; j <= maxValue; j += i) {
                    result[j] = false;
                }
            }
            return result;
        }

        private int ceilMultiple(int k, int n) {
            return k * (int) Math.ceil((double) n / k);
        }
    }
}