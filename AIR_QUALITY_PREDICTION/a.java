import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.functions.RidgeRegression;
import weka.core.Instances;
import weka.core.converters.CSVLoader;
import weka.core.converters.ConverterUtils.DataSource;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.ReplaceMissingValues;
import weka.filters.unsupervised.attribute.Standardize;
import weka.filters.unsupervised.attribute.AddExpression;
import weka.core.Instance;
import java.io.File;

public class RidgeRegressionModel {
    public static void main(String[] args) {
        try {
            // Load data
            CSVLoader loader = new CSVLoader();
            loader.setSource(new File("C:\\Users\\harih\\OneDrive\\Desktop\\PROJECT\\P-2\\datasets\\BOOK2.csv"));
            Instances data = loader.getDataSet();
            System.out.println("Data loaded successfully.");

            // Replace missing values with column means
            ReplaceMissingValues replaceMissingValues = new ReplaceMissingValues();
            replaceMissingValues.setInputFormat(data);
            data = Filter.useFilter(data, replaceMissingValues);
            System.out.println("Missing values filled with column means.");

            // Convert to numeric and remove any non-numeric values
            data.deleteWithMissingClass();

            // Set target variable (AQI) as the last attribute
            data.setClassIndex(data.numAttributes() - 1);

            // Split data into training and testing sets (80% train, 20% test)
            int trainSize = (int) Math.round(data.numInstances() * 0.8);
            int testSize = data.numInstances() - trainSize;
            Instances trainData = new Instances(data, 0, trainSize);
            Instances testData = new Instances(data, trainSize, testSize);
            System.out.println("Data split into training and testing sets.");

            // Standardize the data
            Standardize standardize = new Standardize();
            standardize.setInputFormat(trainData);
            trainData = Filter.useFilter(trainData, standardize);
            testData = Filter.useFilter(testData, standardize);

            // Apply PolynomialFeatures (degree 2 equivalent in Java)
            AddExpression addExpression = new AddExpression();
            addExpression.setExpression("a1*a1+a2*a2+...");  // Adjust expression based on your data structure
            addExpression.setInputFormat(trainData);
            trainData = Filter.useFilter(trainData, addExpression);
            testData = Filter.useFilter(testData, addExpression);

            // Ridge regression model
            RidgeRegression model = new RidgeRegression();
            model.setAlpha(1.0);  // Set alpha manually or use optimization

            // Train the model
            model.buildClassifier(trainData);
            System.out.println("Model training completed.");

            // Evaluate the model
            Evaluation evaluation = new Evaluation(trainData);
            evaluation.evaluateModel(model, testData);

            // Print evaluation metrics
            System.out.println("\nEvaluation Metrics:");
            System.out.printf("Mean Absolute Error: %.2f%n", evaluation.meanAbsoluteError());
            System.out.printf("Mean Squared Error: %.2f%n", evaluation.meanSquaredError());
            System.out.printf("Root Mean Squared Error: %.2f%n", Math.sqrt(evaluation.meanSquaredError()));
            System.out.printf("R-squared: %.2f%n", evaluation.correlationCoefficient() * evaluation.correlationCoefficient());

            // Visualize results - Note: Java doesn't have built-in visualization libraries like Python's Matplotlib or Seaborn
            // Implement custom code or use libraries like JFreeChart for visualization

            // Save the model
            weka.core.SerializationHelper.write("ridge_regression_model.model", model);
            System.out.println("Trained model saved as ridge_regression_model.model");

        } catch (Exception e) {
            System.err.println("An error occurred: " + e.getMessage());
        }
    }
}
