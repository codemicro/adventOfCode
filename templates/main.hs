import System.Environment
import System.Exit
import System.IO
import Data.Maybe
import Data.Char

type ChallengeReturn = Int

one :: String -> ChallengeReturn
one inp = undefined

two :: String -> ChallengeReturn
two inp = undefined

main :: IO ()
main = do args <- getArgs
          inp <- getContents
          _runFn (_selectFn args) inp

_selectFn :: [String] -> Maybe (String -> ChallengeReturn)
_selectFn ["1"] = Just one
_selectFn ["2"] = Just two
_selectFn _ = Nothing

_trimSpace :: String -> String
_trimSpace = f . f
   where f = reverse . dropWhile isSpace

_runFn :: Maybe (String -> ChallengeReturn) -> String -> IO ()
_runFn Nothing _ = _debug "Missing or invalid day argument" >> exitWith (ExitFailure 1)
_runFn (Just fn) inp = putStrLn (show (fn (_trimSpace inp))) >> exitWith ExitSuccess

_debug :: String -> IO ()
_debug x = do hPutStrLn stderr x
