import java.io.*;
import java.util.*;

public class PortfolioStats {

    // Set the exact path to your CSV file here
    static final String CSV_PATH = "/Users/eliemenassa/Desktop/Projet/Projet 3/faang_stocks.csv";

    public static void main(String[] args) throws Exception {
        List<double[]> prices = new ArrayList<>();

        // --- Step 1: Read and parse the CSV file ---
        try (BufferedReader br = new BufferedReader(new FileReader(CSV_PATH))) {
            String line;
            boolean header = true;
            while ((line = br.readLine()) != null) {
                if (header) { header = false; continue; } // skip header
                if (line.trim().isEmpty()) continue;

                // CSV format: Date,AAPL,AMZN,GOOGL,META,NFLX
                String[] p = line.split(",", -1);
                if (p.length < 6) continue; // safety check

                try {
                    double aapl  = Double.parseDouble(p[1]);
                    double amzn  = Double.parseDouble(p[2]);
                    double googl = Double.parseDouble(p[3]);
                    double meta  = Double.parseDouble(p[4]);
                    double nflx  = Double.parseDouble(p[5]);
                    prices.add(new double[]{aapl, amzn, googl, meta, nflx});
                } catch (NumberFormatException ignore) {
                    // skip invalid or missing values
                }
            }
        }

        if (prices.size() < 2) {
            System.out.println("Not enough price data.");
            return;
        }

        // --- Step 2: Compute equal-weighted portfolio prices ---
        List<Double> portfolioPrices = new ArrayList<>(prices.size());
        for (double[] row : prices) {
            double sum = 0;
            for (double v : row) sum += v;
            portfolioPrices.add(sum / row.length);
        }

        // --- Step 3: Compute daily returns r_t = (P_t / P_{t-1}) - 1 ---
        List<Double> returns = new ArrayList<>(portfolioPrices.size() - 1);
        for (int t = 1; t < portfolioPrices.size(); t++) {
            double pt = portfolioPrices.get(t);
            double ptm1 = portfolioPrices.get(t - 1);
            if (ptm1 != 0) returns.add(pt / ptm1 - 1.0);
        }

        if (returns.isEmpty()) {
            System.out.println("No valid returns could be computed.");
            return;
        }

        // --- Step 4: Compute mean and standard deviation ---
        double mean = returns.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        double variance = 0.0;
        for (double r : returns) variance += Math.pow(r - mean, 2);
        variance /= returns.size();
        double std = Math.sqrt(variance);

        // --- Step 5: Display results ---
        System.out.printf("Average daily return: %.4f%% | Daily volatility: %.4f%%%n", mean * 100, std * 100);
        System.out.printf("Annualized return: %.2f%% | Annualized volatility: %.2f%%%n", mean * 252 * 100, std * Math.sqrt(252) * 100);
    }
}

