using PredictCOVIDFinal.Models;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity.Infrastructure;
using System.Linq;
using System.Web;

namespace PredictCOVIDFinal.Service
{
    public class AnalyzeService
    {
        private PREDICT_COVIDEntities db;

        //constructor
        public AnalyzeService()
        {
            this.db = new PREDICT_COVIDEntities();
        }

        // show all predicted
        public List<ANALYZED_PREDICTION> showAllPredict()
        {
            return (from p in db.ANALYZED_PREDICTION where p.PERDICT_PER > 0 orderby p.STATUS descending select p).ToList();
        }

        // add effected
        public void addEffected(String personName, DateTime atTime)
        {
            try
            {
                ANALYZED_PREDICTION host = new ANALYZED_PREDICTION()
                {
                    AT_TIME = atTime,
                    PERDICT_PER = 100,
                    NAME = personName,
                    STATUS = true
                };
                ListOfEffected examList = new ListOfEffected();
                examList.effectedList.Add(host);
                examList.checkedList.Add(host.NAME);
                examList = addPredict(examList, personName, atTime);
                db = new PREDICT_COVIDEntities();
                foreach (var item in examList.effectedList)
                {
                    if(item.NAME == personName)
                    {
                        db.ANALYZED_PREDICTION.Add(item);
                    }
                    else
                    {
                        var comparator = (from p in db.ANALYZED_PREDICTION
                                          where p.NAME == item.NAME
                                          && p.PERDICT_PER <= item.PERDICT_PER
                                          orderby p.AT_TIME ascending
                                          select p).SingleOrDefault();
                        if (comparator == null)
                        {
                            db.ANALYZED_PREDICTION.Add(item);
                        }
                        else
                        {
                            comparator.PERDICT_PER = item.PERDICT_PER;
                        }
                    }
                }
                db.SaveChanges();
            }
            catch (Exception)
            {

                throw;
            }

        }

        /// <summary>
        /// add prediction goes after add effected
        /// </summary>
        /// <param name="personName">host</param>
        /// <param name="atTime">efftected</param>
        private ListOfEffected addPredict(ListOfEffected examList, String personName, DateTime atTime)
        {
            db = new PREDICT_COVIDEntities();
            do
            {
                // initial chceked list 
                if(examList.index == 0)
                {
                    var selected = (from p in db.PREDICTIONs where (p.REF == personName || p.OTHER == personName) && DateTime.Compare(p.AT_TIME, atTime) > 0 select p).ToList();
                    foreach(var i in selected)
                    {
                        String selectedName = "";
                        if (i.REF == personName)
                        {
                            selectedName = i.OTHER;
                        }
                        else
                        {
                            selectedName = i.REF;
                        }
                        if(!isPersonInEffectedList(selectedName, examList.checkedList)) examList.checkedList.Add(selectedName);
                    }
                    examList.index++;
                }
                else
                {
                    String predictName = examList.checkedList[examList.index];
                    var selected = (from p in db.PREDICTIONs where (p.REF == predictName || p.OTHER == predictName)
                                    && DateTime.Compare(p.AT_TIME, atTime) > 0
                                    select p).ToList();
                    double max = 0;
                    DateTime maxTime = new DateTime();
                    foreach(var i in selected)
                    {
                        String selectedName = "";
                        // find other name
                        if (i.REF == predictName)
                        {
                            selectedName = i.OTHER;
                        }
                        else
                        {
                            selectedName = i.REF;
                        }
                        // find maximum percentage
                        if (i.PREDICT_PER > max)
                        {
                            max = i.PREDICT_PER;
                            maxTime = i.AT_TIME;
                        }
                        // check if name is not in the list
                        if(!isPersonInEffectedList(selectedName, examList.checkedList))
                        {
                            examList.checkedList.Add(selectedName);
                        }    
                    }
                    ANALYZED_PREDICTION temp = new ANALYZED_PREDICTION()
                    {
                        AT_TIME = maxTime,
                        PERDICT_PER = max,
                        NAME = predictName,
                        STATUS = false
                    };
                    examList.effectedList.Add(temp);
                    examList.index++;
                }
            }
            while ( examList.index < examList.checkedList.Count);
            return examList;
        }
        private bool isPersonInEffectedList(String name, List<String> effectedList)
        {
            for(int i = 0; i < effectedList.Count; i++)
            {
                if (effectedList[i] == name) return true;
            }
            return false;
        }
        public void removeEffected(String personName)
        {
            var selected = (from p in db.ANALYZED_PREDICTION
                            where p.NAME == personName
                            && p.STATUS == true
                            select p).ToList();
            foreach (var i in selected)
            {
                i.PERDICT_PER = 0;
                i.STATUS = false;
            }
            db.SaveChanges();
        }
    }
}