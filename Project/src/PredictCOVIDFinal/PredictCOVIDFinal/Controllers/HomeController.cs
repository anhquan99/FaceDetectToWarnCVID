using PredictCOVIDFinal.Models;
using PredictCOVIDFinal.Service;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace PredictCOVIDFinal.Controllers
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
        [HttpPost]
        public ActionResult AddUserPost(String name, HttpPostedFileBase[] files)
        {
            try
            {
                foreach(var i in files)
                {
                    if (Path.GetExtension(i.FileName) != "jpg" || Path.GetExtension(i.FileName) != "png") throw new Exception("Wrong file extension");
                }
                bool exists = System.IO.Directory.Exists(getImgPath() + name);
                if (exists) throw new Exception("User already existed");
                Directory.CreateDirectory(getImgPath() + name);
                UserService service = new UserService();
                service.create(new Person()
                {
                    NAME = name,
                    PHOTO = Path.GetFileName(files[0].FileName)
                });
                if (files.Count() > 0)
                {
                    String desPath = this.getImgPath() + name;
                    bool flag = Directory.Exists(desPath);
                    if (flag == false) throw new Exception("Failed to create user folder");
                    foreach (var i in files)
                    {
                        String fileName = Path.GetFileName(i.FileName);

                        String path = Path.Combine(desPath, fileName);
                        i.SaveAs(path);
                    }
                }
                List<String> dataFiles = new List<string>(new String[] { "embeddings.pickle", "le.pickle", "recognizer.pickle" });
                // delete file
                foreach (var i in dataFiles)
                {
                    String dataPath = Path.Combine(getDataPath(), i);
                    if (System.IO.File.Exists(dataPath))
                    {
                        System.IO.File.Delete(dataPath);
                    }
                }
                // create data
                List<String> trainFiles = new List<string>(new String[] { "Embeddings.py", "FaceTrain.py" });
                Process myProcess = new Process();
                myProcess.StartInfo.UseShellExecute = true;
                foreach (var i in trainFiles)
                {
                    String trainPath = Path.Combine(getTrainFilePath(), i);
                    if (System.IO.File.Exists(trainPath))
                    {
                        myProcess.StartInfo.FileName = trainPath;
                        myProcess.StartInfo.CreateNoWindow = false;
                        myProcess.Start();

                    }

                }
                return RedirectToAction("Index", "Home");
            }
            catch (Exception ex)
            {
                ViewBag.mess = ex.Message;
                return View();
            }

        }
        private String getImgPath()
        {
            var dir = AppDomain.CurrentDomain.BaseDirectory;
            dir = dir.Replace("\\src\\PredictCOVIDFinal\\PredictCOVIDFinal\\", "");
            dir += "\\image\\TrainImage\\";
            return dir;
        }
        private String getDataPath()
        {
            var dir = AppDomain.CurrentDomain.BaseDirectory;
            dir = dir.Replace("\\src\\PredictCOVIDFinal\\PredictCOVIDFinal\\", "");
            dir += "\\data\\";
            return dir;
        }
        private String getTrainFilePath()
        {
            var dir = AppDomain.CurrentDomain.BaseDirectory;
            dir = dir.Replace("\\src\\PredictCOVIDFinal\\PredictCOVIDFinal\\", "");
            dir += "\\src\\";
            return dir;
        }
        public ActionResult AddEffected()
        {
            UserService service = new UserService();
            ViewBag.data = service.findNotEffected();
            return View();  
        }
        public ActionResult AddEffectedForm(String name)
        {
            UserService service = new UserService();
            ViewBag.data = service.findByName(name);
            return View();
        }
        [HttpPost]
        public ActionResult AddEffectedPost(String name, DateTime timeEffted)
        {
            try
            {
                UserService service = new UserService();
                var effeted = service.findByName(name);
                AnalyzeService analyzeService = new AnalyzeService();
                analyzeService.addEffected(effeted.NAME, timeEffted);
                return RedirectToAction("Index", "Home");

            }
            catch (Exception ex)
            {
                ViewBag.mess = ex.Message;
                return View();
            }
        }
        public ActionResult removeEffected(String name)
        {
            AnalyzeService service = new AnalyzeService();
            service.removeEffected(name);
            return RedirectToAction("Index", "Home");
        }
    }
}