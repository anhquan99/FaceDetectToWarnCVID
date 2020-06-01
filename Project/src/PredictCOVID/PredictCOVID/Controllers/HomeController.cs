using PredictCOVID.Service;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace PredictCOVID.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            AnalyzeService service = new AnalyzeService();
            ViewBag.data = service.showAllPredict(); 
            return View();
        }
        public ActionResult AddUser()
        {
            return View();
        }
    }
}