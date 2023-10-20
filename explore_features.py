import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def plot_correlation_matrix(df):
    # Compute the correlation matrix
    correlation_matrix = df.iloc[:, 1:].corr()

    # Create a heatmap with no annotations and a smaller font
    plt.figure(figsize=(14, 3))  # Adjust the figure size as needed

    # Create the heatmap without annotations and adjust the font size
    ax =sns.heatmap(correlation_matrix.iloc[:11, :], annot=False, cmap="coolwarm", linewidths=0.5, square=True,
                    xticklabels=1, yticklabels=1, )

    ax.tick_params(axis='both', which='both', labelsize=6)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=60)

    # Set plot title
    plt.title("Correlation Matrix Heatmap")

    # Show the plot
    plt.show()

def plot_pca(df):
    class_labels = df.iloc[:, 1:12]
    names = df.iloc[:, 0]
    features = df.iloc[:, 12:]

    # Perform PCA
    pca = PCA(n_components=2)  # Specify the number of components (2 in this case)
    principal_components = pca.fit_transform(features)

    # Create a DataFrame for the principal components
    pc_df = pd.DataFrame(data=principal_components, columns=["PC1", "PC2"])

    # Create a scatter plot with different colors and marker sizes for each class
    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed

    scale = 10
    pc_df_scaled = scale * pc_df

    # Scatter points with marker sizes and a global alpha value for each class
    for i, row in df.iterrows():
        plt.scatter(
            pc_df_scaled.loc[i, "PC1"],
            pc_df_scaled.loc[i, "PC2"],
            alpha=1.0,
            marker='o',
            facecolor='black',
            s=2
        )

        plt.annotate(
            names[i],
            (pc_df_scaled.loc[i, "PC1"], pc_df_scaled.loc[i, "PC2"]),
            textcoords="offset points",
            xytext=(0,-5),
            ha='center',
            fontsize=4
        )

    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA Plot with Class Labels")

    # Show the plot
    plt.show()

def train(df) -> RandomForestClassifier:
    X = df.iloc[:, 12:]
    y = df.iloc[:, 1:12]
    y = y.replace({True: 1, False: 0})

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")

    return model


# csv built with build_dataset.py
df = pd.read_csv("track_features.csv")

plot_correlation_matrix(df)
plot_pca(df)