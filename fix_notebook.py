#!/usr/bin/env python3
"""
Script to fix issues in R_climatechange.ipynb
"""
import json
import sys

def fix_notebook(input_file, output_file):
    """Apply all fixes to the notebook"""
    with open(input_file, 'r') as f:
        notebook = json.load(f)
    
    cells = notebook['cells']
    
    # Fix 1: Add package installation checks to first code cell
    library_cell = cells[1]
    new_library_source = [
        "# Setup: Install and Load Required Libraries\n",
        "# Function to check and install packages if needed\n",
        "install_if_missing <- function(pkg) {\n",
        "  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {\n",
        "    cat(paste0(\"Installing package: \", pkg, \"\\n\"))\n",
        "    install.packages(pkg, dependencies = TRUE, repos = \"https://cloud.r-project.org\")\n",
        "    library(pkg, character.only = TRUE)\n",
        "  }\n",
        "}\n",
        "\n",
        "# Install required packages\n",
        "required_packages <- c(\"tidyverse\", \"lubridate\", \"ggplot2\", \"gridExtra\", \"grid\", \"zoo\")\n",
        "for (pkg in required_packages) {\n",
        "  install_if_missing(pkg)\n",
        "}\n",
        "\n",
        "# Load Required Libraries\n",
        "library(tidyverse)\n",
        "library(lubridate)\n",
        "library(ggplot2)\n",
        "library(gridExtra)\n",
        "library(grid)\n",
        "library(zoo)\n",
        "\n",
        "# Define Color Palette\n",
        "color1 <- \"#516faa\"\n",
        "color2 <- \"#163542\"\n",
        "color3 <- \"#eaefff\"\n",
        "color4 <- \"#c8d8ef\"\n",
        "color5 <- \"#7d96c1\"\n",
        "\n",
        "# Define Theme\n",
        "my_theme <- theme_minimal() +\n",
        "  theme(\n",
        "    plot.title = element_text(hjust = 0.5, size = 14, face = \"bold\", color = color2),\n",
        "    plot.subtitle = element_text(hjust = 0.5, size = 11, color = color1),\n",
        "    axis.title = element_text(size = 10, color = color2),\n",
        "    panel.grid.major = element_line(color = color3),\n",
        "    panel.grid.minor = element_blank()\n",
        "  )\n",
        "\n",
        "cat(\"Setup complete! All required packages loaded.\\n\")\n"
    ]
    library_cell['source'] = new_library_source
    library_cell['outputs'] = []
    library_cell['execution_count'] = None
    
    # Find the data loading cell (3rd cell, index 3)
    data_cell = cells[3]
    
    # Fix 4 & 2: Better data loading with inspection and placeholder handling
    new_data_source = [
        "# ===== DATA LOADING AND INITIAL INSPECTION =====\n",
        "cat(\"\\n=== Step 1: Loading Data ===\\n\")\n",
        "climate_data <- read.csv(\"climate_change_dataset.csv\", stringsAsFactors = FALSE)\n",
        "\n",
        "# Inspect data structure before processing\n",
        "cat(\"Raw data dimensions:\", nrow(climate_data), \"rows,\", ncol(climate_data), \"columns\\n\")\n",
        "cat(\"\\nFirst few rows (before cleaning):\\n\")\n",
        "print(head(climate_data, 3))\n",
        "\n",
        "# Detect rows with non-numeric Year/Month that cause coercion warnings\n",
        "cat(\"\\n=== Step 2: Checking for Data Quality Issues ===\\n\")\n",
        "year_col <- climate_data[[1]]\n",
        "month_col <- climate_data[[2]]\n",
        "\n",
        "# Find rows with problematic Year/Month values\n",
        "problematic_rows <- which(is.na(suppressWarnings(as.integer(year_col))) | \n",
        "                          is.na(suppressWarnings(as.integer(month_col))))\n",
        "\n",
        "if (length(problematic_rows) > 0) {\n",
        "  cat(\"Found\", length(problematic_rows), \"rows with invalid Year/Month values (rows:\", \n",
        "      paste(problematic_rows, collapse=\", \"), \")\\n\")\n",
        "  cat(\"These rows will be handled during data cleaning.\\n\")\n",
        "}\n",
        "\n",
        "# Rename columns first\n",
        "cat(\"\\n=== Step 3: Renaming Columns ===\\n\")\n",
        "climate_clean <- climate_data %>%\n",
        "  rename(\n",
        "    Year = 1, Month = 2, Avg_Temp = 3, Max_Temp = 4, Min_Temp = 5,\n",
        "    Precipitation = 6, Humidity = 7, Wind_Speed = 8, Solar_Irradiance = 9,\n",
        "    Cloud_Cover = 10, CO2_Concentration = 11, Latitude = 12, Longitude = 13,\n",
        "    Altitude = 14, Proximity_to_Water = 15, Urbanization_Index = 16,\n",
        "    Vegetation_Index = 17, ENSO_Index = 18, Particulate_Matter = 19,\n",
        "    Sea_Surface_Temp = 20\n",
        "  )\n",
        "\n",
        "cat(\"Columns renamed successfully.\\n\")\n",
        "cat(\"Data loaded:\", nrow(climate_clean), \"rows,\", ncol(climate_clean), \"columns\\n\")\n"
    ]
    data_cell['source'] = new_data_source
    data_cell['outputs'] = []
    data_cell['execution_count'] = None
    
    # Add new cell for data cleaning (after data loading)
    cleaning_cell = {
        "cell_type": "code",
        "execution_count": None,
        "id": "data_cleaning_cell",
        "metadata": {"vscode": {"languageId": "r"}},
        "outputs": [],
        "source": [
            "# ===== DATA CLEANING: PLACEHOLDER VALUES =====\n",
            "cat(\"\\n=== Step 4: Detecting and Cleaning Placeholder Values ===\\n\")\n",
            "\n",
            "# Common placeholder values to check\n",
            "placeholder_values <- c(99999, -9999, 999, -999, 9999, -99)\n",
            "\n",
            "# Function to detect placeholder values\n",
            "detect_placeholders <- function(df, placeholders) {\n",
            "  issues <- list()\n",
            "  numeric_cols <- names(df)[sapply(df, is.numeric)]\n",
            "  \n",
            "  for (col in numeric_cols) {\n",
            "    for (placeholder in placeholders) {\n",
            "      problematic_rows <- which(df[[col]] == placeholder)\n",
            "      if (length(problematic_rows) > 0) {\n",
            "        issues[[length(issues) + 1]] <- list(\n",
            "          column = col,\n",
            "          value = placeholder,\n",
            "          rows = problematic_rows\n",
            "        )\n",
            "      }\n",
            "    }\n",
            "  }\n",
            "  return(issues)\n",
            "}\n",
            "\n",
            "# Detect placeholder issues before type conversion\n",
            "cat(\"\\nScanning for placeholder values (99999, -9999, 999, etc.)...\\n\")\n",
            "issues_found <- detect_placeholders(climate_clean, placeholder_values)\n",
            "\n",
            "if (length(issues_found) > 0) {\n",
            "  cat(\"\\n** PLACEHOLDER VALUES DETECTED **\\n\")\n",
            "  for (issue in issues_found) {\n",
            "    cat(sprintf(\"  - Column '%s': value %d found in %d row(s) [%s]\\n\", \n",
            "                issue$column, issue$value, length(issue$rows),\n",
            "                paste(head(issue$rows, 5), collapse=\", \")))\n",
            "    # Replace with NA\n",
            "    climate_clean[[issue$column]][issue$rows] <- NA\n",
            "  }\n",
            "  cat(\"\\nAll placeholder values replaced with NA for proper interpolation.\\n\")\n",
            "} else {\n",
            "  cat(\"No obvious placeholder values detected.\\n\")\n",
            "}\n",
            "\n",
            "# Now perform type conversions with better error handling\n",
            "cat(\"\\n=== Step 5: Type Conversions ===\\n\")\n",
            "climate_clean <- climate_clean %>%\n",
            "  mutate(\n",
            "    Year = suppressWarnings(as.integer(Year)),\n",
            "    Month = suppressWarnings(as.integer(Month)),\n",
            "    across(Avg_Temp:Sea_Surface_Temp, as.numeric)\n",
            "  )\n",
            "\n",
            "# Count NA values introduced\n",
            "na_year <- sum(is.na(climate_clean$Year))\n",
            "na_month <- sum(is.na(climate_clean$Month))\n",
            "\n",
            "if (na_year > 0 || na_month > 0) {\n",
            "  cat(sprintf(\"Type conversion created %d NA values in Year and %d in Month\\n\", \n",
            "              na_year, na_month))\n",
            "  cat(\"These will be handled during Date creation and interpolation.\\n\")\n",
            "}\n",
            "\n",
            "# Create Date column (will have NAs for invalid Year/Month)\n",
            "climate_clean <- climate_clean %>%\n",
            "  mutate(Date = make_date(Year, Month, 1), .after = Month)\n",
            "\n",
            "cat(\"\\nType conversions complete.\\n\")\n",
            "cat(\"Rows with valid dates:\", sum(!is.na(climate_clean$Date)), \"out of\", nrow(climate_clean), \"\\n\")\n"
        ]
    }
    
    # Insert cleaning cell after data loading
    cells.insert(4, cleaning_cell)
    
    # Add markdown cell for data quality report
    quality_report_md = {
        "cell_type": "markdown",
        "id": "data_quality_report",
        "metadata": {},
        "source": [
            "## Data Quality Report\n",
            "\n",
            "### Pre-Cleaning Summary\n",
            "- Placeholder values (99999, -9999, etc.) have been detected and replaced with NA\n",
            "- Type conversion warnings addressed by checking data quality first\n",
            "- Invalid Year/Month values identified and handled\n",
            "\n",
            "### Cleaning Steps Applied\n",
            "1. **Placeholder Detection**: Scanned for common error values (99999, -9999, 999, -999)\n",
            "2. **NA Replacement**: All placeholders replaced with NA before interpolation\n",
            "3. **Type Validation**: Year and Month converted with proper error handling\n",
            "4. **Date Creation**: Valid dates created where possible\n",
            "\n",
            "### Next Steps\n",
            "- Interpolation will handle NA values appropriately\n",
            "- Data validation continues in subsequent cells"
        ]
    }
    
    cells.insert(5, quality_report_md)
    
    # Update the notebook
    notebook['cells'] = cells
    
    # Write the fixed notebook
    with open(output_file, 'w') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    
    print(f"Fixed notebook written to {output_file}")
    print(f"Total cells: {len(cells)}")

if __name__ == "__main__":
    fix_notebook('R_climatechange.ipynb', 'R_climatechange.ipynb')
    print("Notebook fixes applied successfully!")
