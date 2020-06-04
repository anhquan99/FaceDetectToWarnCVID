using PredictCOVIDFinal.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace PredictCOVIDFinal.Service
{
    public class UserService
    {
        public List<Person> findAll()
        {
            using (PREDICT_COVIDEntities db = new PREDICT_COVIDEntities())
            {
                return db.PEOPLE.ToList();
            }
        }
        public bool create(Person p)
        {
            using (PREDICT_COVIDEntities db = new PREDICT_COVIDEntities())
            {
                db.PEOPLE.Add(p);
                if (db.SaveChanges() == 0) return false;
                return true;
            }
        }
        public Person findByName(String personName)
        {
            using (PREDICT_COVIDEntities db = new PREDICT_COVIDEntities())
            {
                var selected = (from p in db.PEOPLE where p.NAME == personName select p).SingleOrDefault();
                return selected;
            }
        }
        public List<Person> findNotEffected()
        {
            using (PREDICT_COVIDEntities db = new PREDICT_COVIDEntities())
            {
                List<Person> notEffectedList = new List<Person>();
                foreach (var i in db.findNotEffected())
                {
                    notEffectedList.Add((from p in db.PEOPLE where p.NAME == i select p).Single());
                }
                return notEffectedList;
            }
        }
    }
}