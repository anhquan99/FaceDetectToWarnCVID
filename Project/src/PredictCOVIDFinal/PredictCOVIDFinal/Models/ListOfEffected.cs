using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace PredictCOVIDFinal.Models
{
    public class ListOfEffected
    {
        public List<ANALYZED_PREDICTION> effectedList { set; get; }
        public List<String> checkedList { set; get; }
        public int index { set; get; }
        public ListOfEffected()
        {
            this.checkedList = new List<string>();
            this.effectedList = new List<ANALYZED_PREDICTION>();
            index = 0;
        }
    }
}