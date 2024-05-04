package java_packages.collections;

public class Pair<K, V> {
    K key;
    V value;

    Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public int compare(Pair<K, V> pair1) {
        return this.hashCode() - pair1.hashCode();
    }

    @Override
    public int hashCode() {
        return this.key.hashCode();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("(");
        sb.append(key);
        sb.append(", ");
        sb.append(value);
        sb.append(")");
        String result = sb.toString();
        return result;
    }
}
