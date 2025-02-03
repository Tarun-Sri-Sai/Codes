import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

class FindGPA {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        String absent = "ab";
        for (int t = Integer.parseInt(br.readLine()); t > 0; t--) {
            int[] credits = new int[6];
            String[] inp = br.readLine().split(" ");
            for (int i = 0; i < 6; i++) {
                credits[i] = Integer.parseInt(inp[i]);
            }
            ScoreSheet[] scores = new ScoreSheet[6];
            for (int i = 0; i < 6; i++) {
                inp = br.readLine().split(" ");
                float[] num = new float[5];
                for (int j = 0; j < 5; j++) {
                    if (inp[j].equals(absent)) {
                        num[j] = 0;
                        continue;
                    }
                    num[j] = Float.parseFloat(inp[j]);
                }
                scores[i] = new ScoreSheet(num[0], num[1], num[2], num[3], num[4], credits[i]);
            }
            float[] points = new float[6];
            for (int i = 0; i < 6; i++) {
                scores[i].calculate_int_score();
                scores[i].calculate_score();
                float gpa_score = scores[i].gpa_score;
                if (gpa_score < 50) {
                    points[i] = 0;
                } else if (gpa_score == 50) {
                    points[i] = 5;
                } else if (gpa_score < 61) {
                    points[i] = 6;
                } else if (gpa_score < 71) {
                    points[i] = 7;
                } else if (gpa_score < 81) {
                    points[i] = 8;
                } else if (gpa_score < 91) {
                    points[i] = 9;
                } else {
                    points[i] = 10;
                }
            }
            float gpa_total = 0, tot_cre = 0;
            String passed = "PASSED, ";
            for (int i = 0; i < 6; i++) {
                gpa_total += points[i];
                System.err.println("Points " + points[i] + " cum " + gpa_total);
                if (!scores[i].passed) {
                    passed = "FAILED, ";
                }
                tot_cre += credits[i];
            }
            gpa_total /= tot_cre;
            bw.write(passed + gpa_total + "\n");
        }
        bw.flush();
    }
}

class ScoreSheet {
    public float int1, int2, int3, fin, att, int_avg, gpa_score = 0, points;
    public float credits;
    public boolean passed = true;

    public ScoreSheet(float int1, float int2, float int3, float fin, float att, float credits) {
        this.int1 = int1;
        this.int2 = int2;
        this.int3 = int3;
        this.fin = fin;
        this.att = att;
        this.credits = credits;
    }

    public void calculate_int_score() {
        float num1 = this.int1, num2 = this.int2, num3 = this.int3;
        this.int_avg = num1 > num2 ? (num2 > num3 ? num2 : num3) + num1 : (num1 > num3 ? num1 : num3) + num2;
    }

    public void calculate_score() {
        this.gpa_score += this.credits * ((this.int_avg * ((float) 45 / 100)) + (this.fin * ((float) 50 / 100))
                + (calculate_attscore(this.att) * ((float) 5 / 100)));
        if (this.gpa_score < 50) {
            passed = false;
        }
    }

    private static int calculate_attscore(float att) {
        if (att < 51) {
            return 5;
        }
        if (att < 61) {
            return 4;
        }
        if (att < 71) {
            return 3;
        }
        if (att < 81) {
            return 2;
        }
        if (att < 91) {
            return 1;
        }
        return 0;
    }
}

/*
 * 1
 * 1 1 1 2 2 3
 * 19 18 20 70 70
 * 17.33 15 16.66 66 70.66
 * ab ab ab 0 100
 * ab ab 10 78 78
 * 17 18.33 19.5 64 87
 * 14 8 ab 60 45
 */