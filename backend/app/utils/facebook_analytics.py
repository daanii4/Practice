import os
import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from app.models import Project
from app.database import get_db
from dotenv import load_dotenv
from sqlalchemy import Column, Float, Integer, String, ForeignKey

# Load environment variables
load_dotenv()

FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")



ctr = Column(Float, default=0.0)
cpa = Column(Float, default=0.0)
roas = Column(Float, default=0.0)
engagement_rate = Column(Float, default=0.0)
conversions = Column(Integer, default=0)


def fetch_facebook_ad_performance(project_id: int, db: Session = Depends(get_db)):
    # Fetch project from the database
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Facebook Ads API endpoint to fetch ad performance
    url = f"https://graph.facebook.com/v12.0/act_{AD_ACCOUNT_ID}/ads"
    params = {
        "access_token": FACEBOOK_ACCESS_TOKEN,
        "fields": "id,name,adset_id,adset_name,clicks,impressions,ctr,spend,actions,conversion_rate_ranking,cost_per_action_type,return_on_ad_spend",
        "date_preset": "last_30d"  # You can adjust the date range as needed
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get("data", [])
        
        if not data:
            return {"message": "No ad performance data available for this project"}

        # Example of selecting the first ad's data if multiple ads are present
        ad_performance = data[0]
        
        # Extract relevant analytics data
        ctr = ad_performance.get("ctr", "N/A")
        spend = ad_performance.get("spend", "N/A")
        roas = ad_performance.get("return_on_ad_spend", {}).get("value", "N/A")
        actions = ad_performance.get("actions", [])
        cost_per_action = ad_performance.get("cost_per_action_type", [])
        conversion_rate_ranking = ad_performance.get("conversion_rate_ranking", "N/A")

        conversions = next((action["value"] for action in actions if action["action_type"] == "offsite_conversion"), "N/A")
        cpa = next((cpa["value"] for cpa in cost_per_action if cpa["action_type"] == "offsite_conversion"), "N/A")

        # Update project with fetched analytics
        project.ctr = float(ctr) if ctr != "N/A" else None
        project.cpa = float(cpa) if cpa != "N/A" else None
        project.roas = float(roas) if roas != "N/A" else None
        project.engagement_rate = ad_performance.get("engagement_rate", 0.0)
        project.conversions = int(conversions) if conversions != "N/A" else 0
        db.commit()

        # Return the detailed data the user will see
        return {
            "project_id": project_id,
            "ad_name": ad_performance.get("name", "N/A"),
            "adset_name": ad_performance.get("adset_name", "N/A"),
            "impressions": ad_performance.get("impressions", "N/A"),
            "clicks": ad_performance.get("clicks", "N/A"),
            "ctr": ctr,
            "spend": spend,
            "conversions": conversions,
            "cpa": cpa,
            "roas": roas,
            "conversion_rate_ranking": conversion_rate_ranking
        }
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch analytics from Facebook: {response.json().get('error', {}).get('message', 'Unknown error')}")
