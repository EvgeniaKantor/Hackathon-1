import pandas as pd

class AudienceProfile:
    def __init__(self, df_audience):
        self.df = df_audience
        self.profile = self.create_profile()
    
    def create_profile(self):
        most_popular_age = self.df['Age'].mode()[0]
        most_popular_gender = self.df['Gender'].mode()[0]
        most_popular_skin_type = self.df[['Skin Type_Combination', 'Skin Type_Dry', 
                                          'Skin Type_Normal', 'Skin Type_Oily', 
                                          'Skin Type_Sensitive']].sum().idxmax().split('_')[1]
        feature_cols = ['Anti-acne', 'Anti-aging', 'Hydrating', 
                        'Anti-dark spots', 'Day Care', 'Night Care', 'Sun Protect']
        most_popular_features = self.df[feature_cols].sum().sort_values(ascending=False).head(3).index.tolist()
        
        return {
            'Age': most_popular_age,
            'Gender': most_popular_gender,
            'Skin Type': most_popular_skin_type,
            'Cosmetic Features': most_popular_features
        }
    
    def get_profile(self):
        return self.profile


class CosmeticProduct:
    def __init__(self, name, brand, price, rank, skin_types, features):
        self.name = name
        self.brand = brand
        self.price = price
        self.rank = rank
        self.skin_types = skin_types
        self.features = features
    
    def matches_audience(self, audience_profile):
        if audience_profile['Skin Type'] not in self.skin_types:
            return False  
        audience_features = set(audience_profile['Cosmetic Features'])
        product_features = {feature for feature, value in self.features.items() if value > 0}
        return audience_features.issubset(product_features)  
    
    def get_skin_type_list(self):
        return [skin for skin, value in self.skin_types.items() if value > 0]

    def get_feature_list(self):
        return [feature for feature, value in self.features.items() if value > 0]


class SynchroCosmetics:
    def __init__(self, df_audience, df_cosmetic):
        self.audience = AudienceProfile(df_audience)
        self.audience_profile = self.audience.get_profile()
        self.df_cosmetic = df_cosmetic
        self.products = self.load_products(df_cosmetic)
    
    def load_products(self, df_cosmetic):
        products = []
        for _, row in df_cosmetic.iterrows():
            skin_types = {key: row[key] for key in ["Combination", "Dry", "Normal", "Oily", "Sensitive"]}
            features = {key: row[key] for key in ["Anti-acne", "Anti-aging", "Hydrating", "Anti-dark spots", "Day Care", "Night Care", "Sun Protect"]}
            product = CosmeticProduct(row["Name"], row["Brand"], row["Price"], row["Rank"], skin_types, features)
            products.append(product)
        return products
    
    def get_recommendations(self, top_n=5):
        matching_products = [p for p in self.products if p.matches_audience(self.audience_profile)]
        sorted_products = sorted(matching_products, key=lambda p: p.rank, reverse=True)
        return sorted_products[:top_n], len(matching_products)  
    
    def display_recommendations(self, top_n=5, save_to_file=False):
        recommendations, total_matching = self.get_recommendations(top_n)
        output_lines = []
        
        output_lines.append("\n🔹 **Audience Profile** 🔹")
        for key, value in self.audience_profile.items():
            output_lines.append(f"  - {key}: {value}")
        
        output_lines.append(f"\n✅ Total Fit Products: {total_matching}")

        if not recommendations:
            output_lines.append("\n❌ No matching products found.")
        else:
            output_lines.append("\n🔹 **Top Cosmetic Recommendations** 🔹")
            for i, product in enumerate(recommendations, start=1):
                product_label = self.df_cosmetic.loc[self.df_cosmetic["Name"] == product.name, "Label"].values
                product_type = product_label[0] if len(product_label) > 0 else "Unknown"
                skin_types = ", ".join(product.get_skin_type_list())
                features = ", ".join(product.get_feature_list())
                
                output_lines.append(f"""{i}. {product.name} by {product.brand}  
   - Type: {product_type}  
   - Rank: {product.rank}, Price: ${product.price}  
   - Suitable for: {skin_types} skin  
   - Features: {features}""")
        
        result_text = "\n".join(output_lines)
        print(result_text)
        
        if save_to_file:
            with open("recommendations.txt", "w", encoding="utf-8") as file:
                file.write(result_text)


# Load Data
df_audience = pd.read_excel(r'Week4\Hackathon\audience_data.xlsx')
df_cosmetic = pd.read_excel(r'Week4\Hackathon\cosmetic_data.xlsx')

# Create Recommendation System
synchro = SynchroCosmetics(df_audience, df_cosmetic)

# Show Recommendations and Save to File
synchro.display_recommendations(top_n=5, save_to_file=True)