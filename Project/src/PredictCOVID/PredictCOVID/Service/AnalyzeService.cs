using PredictCOVID.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace PredictCOVID.Service
{
    public class AnalyzeService
    {
        private PREDICT_COVIDEntities db;
        public AnalyzeService()
        {
            this.db = new PREDICT_COVIDEntities();
        }
        public List<ANALYZED_PREDICTION> showAllPredict()
        {
            return (from p in db.ANALYZED_PREDICTION where p.PERDICT_PER > 0 select p).ToList();
        }
        public void addEffected(String personName, DateTime atTime)
        {
            db.ANALYZED_PREDICTION.Add(new ANALYZED_PREDICTION()
            {
                AT_TIME = atTime,
                PERDICT_PER = 100,
                NAME = personName,
                STATUS = true
            });
            var list = (from p in db.PREDICTIONs
                        where p.REF == personName 
                        && p.OTHER == personName 
                        && DateTime.Compare(p.AT_TIME, atTime) > 1
                        select p).ToList();
            foreach(var i in list)
            {
                String selectedName = (i.REF == personName) ? i.OTHER : i.REF;
                addPredict(db, selectedName, atTime);
            }
        }
        private void addPredict(PREDICT_COVIDEntities db, String personName, DateTime atTime)
        {
            List<PREDICTION> list = (from p in db.PREDICTIONs
                                     where DateTime.Compare(p.AT_TIME, atTime) > 1 
                                     && (p.REF == personName || p.OTHER == personName)
                                     select p).ToList();
            foreach( var i in list)
            {
                String selectedName = "";
                if(i.REF == personName)
                {
                    selectedName = i.OTHER;
                }
                else
                {
                    selectedName = i.REF;
                }
                var existed = (from p in db.ANALYZED_PREDICTION
                               where p.NAME == selectedName
                               && DateTime.Compare(p.AT_TIME, atTime) > 1
                               orderby p.AT_TIME
                               select p).SingleOrDefault();
                if (existed == null)
                {
                    ANALYZED_PREDICTION temp = new ANALYZED_PREDICTION()
                    {
                        AT_TIME = i.AT_TIME,
                        NAME = selectedName,
                        STATUS = false,
                        PERDICT_PER = i.PREDICT_PER
                    };
                    db.ANALYZED_PREDICTION.Add(temp);
                    db.SaveChanges();
                }
                else
                {
                    if (existed.PERDICT_PER < i.PREDICT_PER)
                    {
                        existed.PERDICT_PER = i.PREDICT_PER;
                        db.SaveChanges();
                    }
                }
                addPredict(db, selectedName, i.AT_TIME);
            }
        }
        public void removeEffected(String personName)
        {
            var selected = (from p in db.ANALYZED_PREDICTION
                            where p.NAME == personName 
                            && p.STATUS == true
                            select p).ToList();
            foreach(var i in selected)
            {
                i.PERDICT_PER = 0;
                i.STATUS = false;
            }
            db.SaveChanges();
        }
    }
}