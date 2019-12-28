import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from collections import OrderedDict
from operator import itemgetter



# read in csv and convert to dataframe
# dataset downloaded from: https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Physician-and-Other-Supplier2017

medicaredf = pd.read_csv(r"/Users/briananderson/Desktop/Medicare2017b.txt", sep="\t", header=None,
                         names=("npi", "nppes_provider_last_org_name", "nppes_provider_first_name",
                                "nppes_provider_mi", "nppes_credentials", "nppes_provider_gender",
                                "nppes_entity_code", "nppes_provider_street1", "nppes_provider_street2",
                                "nppes_provider_city", "nppes_provider_zip", "nppes_provider_ruca",
                                "nppes_provider_state", "nppes_provider_country", "provider_type",
                                "medicare_participation_indicator",
                                "number_of_hcpcs", "total_services", "total_unique_benes", "total_submitted_chrg_amt",
                                "total_medicare_allowed_amt", "total_medicare_payment_amt", "total_medicare_stnd_amt",
                                "drug_suppress_indicator", "number_of_drug_hcpcs", "total_drug_services",
                                "total_drug_unique_benes",
                                "total_drug_submitted_chrg_amt", "total_drug_medicare_allowed_amt",
                                "total_drug_medicare_payment_amt",
                                "total_drug_medicare_stnd_amt", "med_suppress_indicator", "number_of_med_hcpcs",
                                "total_med_services",
                                "total_med_unique_benes", "total_med_submitted_chrg_amt",
                                "total_med_medicare_allowed_amt",
                                "total_med_medicare_payment_amt", "total_med_medicare_stnd_amt",
                                "beneficiary_average_age", "beneficiary_age_less_65_count",
                                "beneficiary_age_65_74_count", "beneficiary_age_75_84_count",
                                "beneficiary_age_greater_84_count",
                                "beneficiary_female_count", "beneficiary_male_count", "beneficiary_race_white_count",
                                "beneficiary_race_black_count",
                                "beneficiary_race_api_count", "beneficiary_race_hispanic_count",
                                "beneficiary_race_natind_count",
                                "beneficiary_race_other_count", "beneficiary_nondual_count", "beneficiary_dual_count",
                                "beneficiary_cc_afib_percent",
                                "beneficiary_cc_alzrdsd_percent", "beneficiary_cc_asthma_percent",
                                "beneficiary_cc_cancer_percent",
                                "beneficiary_cc_chf_percent", "beneficiary_cc_ckd_percent",
                                "beneficiary_cc_copd_percent", "beneficiary_cc_depr_percent",
                                "beneficiary_cc_diab_percent", "beneficiary_cc_hyperl_percent",
                                "beneficiary_cc_hypert_percent",
                                "beneficiary_cc_ihd_percent", "beneficiary_cc_ost_percent",
                                "beneficiary_cc_raoa_percent",
                                "beneficiary_cc_schiot_percent", "beneficiary_cc_strk_percent",
                                "Beneficiary_Average_Risk_Score"))

medicare_csv = medicaredf.to_csv(r"/Users/briananderson/Desktop/Medicare2017.csv", index=None, header=True)


# change output settings
pd.set_option("display.width", 2000)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 2000000)

# read in file
medicare_df = pd.read_csv("Medicare_filtered_12.26.19.csv")

# update all NaN to 0
medicare_df = medicare_df.fillna(0)
for col in medicare_df.columns:
    print(col)


# convert column to a list
providers = medicare_df.PROVIDER.tolist()

# descending prevalence of providers
provider_list = Counter(providers)

# select 10 most common providers
pl = provider_list.most_common(10)

labels = [i[0] for i in pl] # first item in list
sizes = [i[1] for i in pl] # 2nd item in list

# pie chart with text in legend only
patches, texts = plt.pie(sizes, startangle=90, explode=(0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0)) # explode out DC piece
plt.title("Top 20 Provider Types Medicare 2017")
plt.legend(patches, labels, bbox_to_anchor=(1, 1), loc="upper left", fontsize=10)
plt.tight_layout()
plt.show()

# create new dataframe using only chronic disease columns
chronic_disease_df = medicare_df[["AFIB%","ALZHEIMERS%","ASTHMA%","CANCER%","CHF%","KIDNEYDZ%","COPD%","DEPRESS%","DM%",
"HYPERLIPID%","HTN%","IHD%","OST%","RA/OA%","SCHIZO/OTHERPSYCH%","STROKE%"]].copy()

# get mean % for each disease
mean_dz = chronic_disease_df.apply(np.mean)

# most to least common
order = OrderedDict(sorted(mean_dz.items(), key=itemgetter(1), reverse=True))

# bar chart
plt.bar(range(len(order)), order.values(), align="center")
plt.xticks(range(len(order)), list(order.keys()))
plt.xticks(rotation=90)
plt.ylabel("Mean percentage")
plt.title("Mean percentage of each chronic disease")
plt.show()

# PROVIDER TYPE/ RISK SCORE CORRELATION

provider_riskscore_df = medicare_df[["PROVIDER", "AVERISKSCORE"]].copy()

# convert df to list
provider_riskscore_list = provider_riskscore_df.PROVIDER.tolist()

# select x most common provider types
provider_riskscore_lists = Counter(provider_riskscore_list).most_common(x)
prl = provider_riskscore_lists.mostcommon(x)

# create dictionary with provider as key and risk score as value
df_to_dict = pd.Series(provider_riskscore_df.AVERISKSCORE.values, index=provider_riskscore_df.PROVIDER).to_dict()

from collections import OrderedDict
from operator import itemgetter

# sort dictionary by most common key
ordered = OrderedDict(sorted(df_to_dict.items(), key=itemgetter(1), reverse=True))

# shorten names of specialties (easier to read in graph form)
ordered["Transplant Cardiology"] = ordered.pop("Advanced Heart Failure and Transplant Cardiology")
ordered["Stem Cell Transplant"] = ordered.pop("Hematopoietic Cell Transplantation and Cellular Therapy")
ordered["Nurse Anesthetist"] = ordered.pop("Certified Registered Nurse Anesthetist (CRNA)")
ordered["Dietition"] = ordered.pop("Registered Dietitian or Nutrition Professional")
ordered["Speech Pathologist"] = ordered.pop("Speech Language Pathologist")
ordered["Osteopathic Manipulation"] = ordered.pop("Osteopathic Manipulative Medicine")
ordered["Vascular Disease"] = ordered.pop("Peripheral Vascular Disease")
ordered["Hospice"] = ordered.pop("Hospice and Palliative Care")
ordered["Ambulance"] = ordered.pop("Ambulance Service Provider")
ordered["Intensivists"] = ordered.pop("Critical Care (Intensivists)")
ordered["Proctology"] = ordered.pop("Colorectal Surgery (Proctology)")


# select top x provider:risk score pairs (non-providers were eliminated from csv file)
top_twenty_five = dict(list(ordered.items())[:x])

# plot results
plt.bar(range(len(top_twenty_five)), top_twenty_five.values(), align="center")
plt.xticks(range(len(top_twenty_five)), list(top_twenty_five.keys()))
plt.xticks(rotation=90)
plt.ylabel("Mean Risk Score")
plt.title("Mean risk score in each specialty")
plt.show()



