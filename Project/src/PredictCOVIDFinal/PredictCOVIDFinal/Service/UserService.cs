using PredictCOVIDFinal.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace PredictCOVIDFinal.Service
{
    public class UserService
    {
        private PREDICT_COVIDEntities db;
        public List<Person> findAll()
        {
            return db.PEOPLE.ToList();
        }
        public bool create(Person p)
        {
            db.PEOPLE.Add(p);
            if (db.SaveChanges() == 0) return false;
            return true;
        }
        public Person findByName(String personName)
        {
            var selected = (from p in db.PEOPLE where p.NAME == personName select p).SingleOrDefault();
            return selected;
        }
        public UserService()
        {
            this.db = new PREDICT_COVIDEntities();
        }
        public List<Person> findNotEffected()
        {
            List<Person> notEffectedList = new List<Person>();
            foreach(var i in db.findNotEffected())
            {
                notEffectedList.Add((from p in db.PEOPLE where p.NAME == i select p).Single());
            }
            return notEffectedList;
        }
    }
}